$(document).on("click", ".card-summary",
  function(event) {
    var content = $(event.target).parent().find(".card-content");
    $(event.target).toggleClass("content-visible");
    if(content != null) {
      var expand_icon = $(event.target).find(".card-expand>i");
      expand_icon.toggleClass("fa-chevron-down");
      expand_icon.toggleClass("fa-chevron-up");
      content.slideToggle("ease-in");
    }
  }
);

/* Closing panels */
$(document).on("click", ".close",
  function(event) {
    var panel = $(event.target).closest(".panel");
    var panelClone = panel.clone();
    var cancel_close_button = "<div><a class=\"btn wire discreet panelCloseCancel\">Cancel</a></div>";
    html = $(cancel_close_button).append(panelClone);
    panelClone.hide();
    panel.replaceWith(html);
    setTimeout(function() {
      html.find(".panelCloseCancel").fadeOut();
    }, 2000);
  }
);


$(document).on("click", ".panelCloseCancel", function(event) {
  var panel = $(event.target).parent().find(".panel").clone();
  $(event.target).replaceWith(panel.show());
});
