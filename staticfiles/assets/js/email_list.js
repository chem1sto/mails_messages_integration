let ws;
$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email");
    if (!email) {
        alert("Требуется электронная почта");
        window.location.href = "/";
        return;
    }

    const webSocketProtocol = window.location.protocol.includes('https') ? 'wss' : 'ws';
    ws = new WebSocket(`${webSocketProtocol}://${window.location.host}/ws/email_list/`);
    let totalEmails = 0;
    let loadedEmails = 0;
    let checkedEmails = 0;
    let loadingStarted = false;

    ws.onopen = () => {
        console.log("WebSocket connection opened");
        ws.send(JSON.stringify({ action: "fetch_emails", email: email }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "total_emails") {
            totalEmails = data.total;
            updateProgressBar(loadedEmails, checkedEmails, totalEmails);
        } else if (data.type === "new_email") {
            loadingStarted = true;
            const email = data.email_data;
            const row = $("<tr>");
            row.append($("<td>").text(email.subject));
            const from = email.from;
            const fromParts = from.match(/(.*?) <(.*?)>/);
            const fromName = fromParts ? fromParts[1].trim() : from;
            const fromEmail = fromParts ? fromParts[2].trim() : from;
            const fromCell = $("<td>").append(
                $("<div>").text(fromName),
                $("<div>").append(
                    $("<a>").attr("href", "#").text(fromEmail).on("click", function(e) {
                        e.preventDefault();
                        window.open(`mailto:${fromEmail}`, "_blank");
                    })
                )
            );
            row.append(fromCell);
            row.append($("<td>").addClass("centered").text(email.date));
            row.append($("<td>").addClass("centered").text(email.received));
            row.append($("<td>").text(email.text));
            const attachmentsCell = $("<td>").addClass("centered");
            if (email.attachments && email.attachments.length > 0) {
                email.attachments.forEach(attachment => {
                    const attachmentLink = $("<a>")
                        .attr("href", attachment.url)
                        .text(attachment.filename)
                    attachmentsCell.append(attachmentLink).append("<br>");
                });
            } else {
                attachmentsCell.text("Нет вложений");
            }
            row.append(attachmentsCell);
            $("#email-table tbody").append(row);
            loadedEmails++;
            updateProgressBar(loadedEmails, checkedEmails, totalEmails);
        } else if (data.type === "progress") {
            checkedEmails = data.checked;
            updateProgressBar(loadedEmails, checkedEmails, totalEmails);
        } else if (data.type === "error") {
            $("#error-message").text(data.message);
        }
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
        console.log("WebSocket connection closed");
    };

    function updateProgressBar(loaded, checked, total) {
        if (loadingStarted) {
            $("#progress-bar").removeClass("checking");
            $("#progress-bar").width(`${(loaded / total) * 100}%`);
            $("#progress-bar").text(`Загружено писем: ${total - loaded}`);
        } else {
            $("#progress-bar").addClass("checking");
            $("#progress-bar").text(`Проверено писем: ${checked}/${total}`);
        }
    }
});

function closeWebSocketAndNavigate() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "close_connection" }));
    }
    window.location.href = "/";
}
