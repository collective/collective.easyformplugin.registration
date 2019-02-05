require(["jquery", "mockup-i18n"], function($, I18N) {
  "use strict";

  $(document).ready(function() {
    var generateHtml = function(name) {
      var html = "";
      html += '<span class="option">';
      html +=
        '<input id="select-all-' +
        name +
        '" name="select-all-' +
        name +
        '" class="checkbox-widget tuple-field" type="checkbox">';
      html += '<label for="select-all-' + name + '">';
      html +=
        '<span class="label">&nbsp;' + _t("label_select_all_items") + "</span>";
      html += "</label>";
      html += "</span>";
      return html;
    };

    var i18n = new I18N();
    i18n.loadCatalog("plone");
    var _t = i18n.MessageFactory("plone");

    $("#form-widgets-registrants").before(generateHtml("registrants"));
    $("#form-widgets-waiting_list").before(generateHtml("waiting_list"));

    $("#select-all-registrants").click(function(e) {
      $("#form-widgets-registrants input:checkbox").prop(
        "checked",
        e.target.checked
      );
    });
    $("#select-all-waiting_list").click(function(e) {
      $("#form-widgets-waiting_list input:checkbox").prop(
        "checked",
        e.target.checked
      );
    });
  });
});
