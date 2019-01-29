function updateRelevance(query, doc, id) {
    var btn = $("#button" + id);
    var rel = 0;
    if (btn.text() == "Not relevant") {
        btn.text("Relevant");
        rel = 1;
    } else {
        btn.text("Not relevant");
        rel = 0;
    }
    btn.toggleClass("btn-success");
    btn.toggleClass("btn-danger");
    $.get({
        url: "annotate?query=" + query + "&docid=" + doc + "&rel=" + rel
    });
}
