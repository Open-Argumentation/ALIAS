$(function(){

    setupFrameworkList();

});

var frameworks = ['af1', 'af2', 'af3', 'af4', 'af5', 'af6'];

function setupFrameworkList() {
    var myList = $('#example_frameworks');
    myList.empty();

    $.each(frameworks, function (i) {
        var li = $('<li/>')
            .attr('id', frameworks[i])
            .appendTo(myList);

        var aa = $('<a/>')
            .text(frameworks[i])
            .appendTo(li);
    });

    $('#example_frameworks li').click(function () {
        $.post('/framework/' + this.id, function (data) {
            var cy = cytoscape({
                container: $('#cy'),
            });

            var json = $.parseJSON(data)
            console.log(json['arguments'])

            $.each(json['arguments'], function(i, obj) {
                cy.add({
                    data: {id: obj['name'], label: obj['name']}
                })
            });

            $.each(json['arguments'], function(i, obj) {
                $.each(obj['attacks'], function(j, attack) {
                    cy.add({
                        data: {
                            id: 'edge_' + obj['name'] + '_' + attack + '_' + i + j,
                            source: obj['name'],
                            target: attack,
                        }
                    });
                })
            });

            cy.layout({name: 'cola',
                    infinite: true,
                    fit: false,})
        });
    });
}
