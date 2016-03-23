$(document).on("click", ".card-summary.active",
    function (event) {
        var card = $(event.target).closest(".card");
        var content = card.find(".card-content");
        $(event.target).toggleClass("content-visible");
        if (content != null) {
            var expand_icon = card.find(".card-expand>i");
            card.toggleClass("displaying");
            expand_icon.toggleClass("fa-chevron-down");
            expand_icon.toggleClass("fa-chevron-up");
            content.slideToggle("ease-in");
        }
    }
);

/* Closing dismissables */
$(document).on("click", ".close",
    function (event) {
        var dismissible = $(event.target).closest(".dismissible");
        if (dismissible.hasClass("panel")) {
            var panelClone = dismissible.clone();
            var cancel_close_button = "<div><a class=\"btn wire discreet panelCloseCancel\">Cancel</a></div>";
            html = $(cancel_close_button).append(panelClone);
            panelClone.hide();
            dismissible.replaceWith(html);
            setTimeout(function () {
                html.find(".panelCloseCancel").fadeOut();
            }, 2000);
        } else {
            dismissible.remove();
        }
    }
);


$(document).on("click", ".panelCloseCancel", function (event) {
    var panel = $(event.target).parent().find(".panel").clone();
    $(event.target).replaceWith(panel.show());
});