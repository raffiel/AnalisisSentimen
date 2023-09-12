$(".nav-tabs a").click(function () {
  $(this).tab("show");
});

$('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
  var target = $(e.target).attr("href"); // aktifkan tab-pane yang sesuai
  $(target).fadeIn("slow");
});
$('a[data-toggle="tab"]').on("hide.bs.tab", function (e) {
  var target = $(e.target).attr("href"); // nonaktifkan tab-pane yang sesuai
  $(target).fadeOut("slow");
});
