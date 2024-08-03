let ws;
$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email");
    if (email) {
        ws = new WebSocket(`ws://${window.location.host}/ws/email_list/`);
        let totalEmails = 0;
        let loadedEmails = 0;
        ws.onopen = () => {
            ws.send(JSON.stringify({ action: "fetch_emails", email: email }));
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "total_emails") {
                totalEmails = data.total;
                updateProgressBar(loadedEmails, totalEmails);
            } else if (data.type === "email_list") {
                const emails = data.email;
                emails.forEach(email => {
                    const row = $("<tr>");
                    row.append($("<td>").addClass("centered").text(email.subject));
                    row.append($("<td>").addClass("centered").text(email.from));
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
                    updateProgressBar(loadedEmails, totalEmails);
                });
            } else if (data.type === "error") {
                $("#error-message").text(data.message);
            }
        };
    } else {
        alert("Требуется электронная почта");
        window.location.href = "/";
    }
    function updateProgressBar(loaded, total) {
        const progress = (loaded / total) * 100;
        $("#progress-bar").width(`${progress}%`);
        $("#progress-bar").text(`${progress.toFixed(2)}%`);
    }
});
function closeWebSocketAndNavigate() {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "close_connection" }));
    }
    window.location.href = "/";
}
