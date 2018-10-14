$(function(){

    setupFrameworkList();
    setupExtensions();
    enableExtensions();
});

var is_framework = false;
var frameworks = ['af1', 'af2', 'af3', 'af4', 'af5', 'af6'];
var extensions = ['Complete', 'Stable', 'Preferred'];
var selected_extension = '';
var cy;

function setupFrameworkList() {
    var myList = $('#example_frameworks');
    myList.empty();

    $.each(frameworks, function (i) {
        var aa = $('<a/>')
            .addClass('dropdown-item')
            .attr('id', frameworks[i])
            .text(frameworks[i])
            .appendTo(myList);
    });

    $('#example_frameworks a').click(function () {
        $('.sol_list').empty();
        $.post('/framework/' + this.id, function (data) {

            var json = $.parseJSON(data)
            cy = cytoscape({
                container: $('#cy'),
                style: [
                    {
                        selector: '.node_sol',
                        style: {
                            'background-color': 'green',
                        }
                    },
                    {
                        selector: 'node',
                        style: {
                            'label': 'data(label)',
                            'border': 'grey',
                            'labelValign': 'center',
                            'labelHalign': 'center',
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'curve-style': 'bezier',
                            'width': 3,
                            'line-color': '#ccc',
                            'target-arrow-color': '#ccc',
                            'target-arrow-shape': 'triangle'
                        }
                    }

                ]
            });

            $.each(json['arguments'], function(i, obj) {
                cy.add({
                    data: {
                        id: obj['name'],
                        label: obj['name']
                    }
                });
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

            cy.layout({
                name: 'cola',
                    infinite: true,
                    fit: false,
            });

            is_framework = true;
            enableExtensions();
        });
    });
}

function enableExtensions()
{
    if (is_framework)
    {
        $('.ext_element').removeClass('disabled');
    }
    else
    {
        $('.ext_element').addClass('disabled');
    }
}

function setupExtensions()
{
    var myList = $('#extensions');
    $.each(extensions, function (i) {
        var aa = $('<a/>')
            .text(extensions[i])
            .attr('id', extensions[i])
            .addClass('ext_element')
            .addClass('dropdown-item')
            .appendTo(myList);
    });

    $('#extensions a').click(function () {
        selected_extension = this.id;
        $.post('/extension/' + this.id, function (data) {
            var jsonReturn = $.parseJSON(data);

            $('#sol_title').text('Solution: ' + selected_extension + ' extensions')

            $('.sol_list').empty();

            $.each(jsonReturn, function(i, item) {
                $('<a/>')
                    .text(item)
                    .addClass('list-group-item')
                    .addClass('list-group-item-action')
                    .addClass('solution_item')
                    .attr('id', 'solution' + i)
                    .appendTo($('.sol_list'));
            })

            $('.solution_item').click(function()
            {
                cy.$('.node_sol').removeClass('node_sol');

                var sol = $('#' + this.id).text().split(',');
                $.each(sol, function(i, item)
                {
                    cy.$('#' + item).addClass('node_sol');
                })
            })
        });
    });
}
