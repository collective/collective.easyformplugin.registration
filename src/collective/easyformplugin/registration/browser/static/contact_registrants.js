$(document).ready(function () {
  var generateHtml = function (name) {
    var html = "<br>";
    html += '<span class="option">';
    html +=
      '<input id="select-all-' +
      name +
      '" name="select-all-' +
      name +
      '" class="checkbox-widget tuple-field" type="checkbox">';
    html += '<label for="select-all-' + name + '">';
    html += '<span class="label">&nbsp;Select all</span>';
    html += "</label>";
    html += "</span>";
    html += "<br>";
    return html;
  };

  $("#form-widgets-registrants").before(generateHtml("registrants"));
  $("#form-widgets-waiting_list").before(generateHtml("waiting_list"));

  $("#select-all-registrants").click(function (e) {
    $("#form-widgets-registrants input:checkbox").prop(
      "checked",
      e.target.checked,
    );
  });
  $("#select-all-waiting_list").click(function (e) {
    $("#form-widgets-waiting_list input:checkbox").prop(
      "checked",
      e.target.checked,
    );
  });
});
