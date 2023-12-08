let compareTable = (function () {

    var _tableId, _table,
        _fields, _headers,
        _defaultText;

    /** Builds the row with columns from the specified names.*/
    function _buildCompareRowColumns(names, item, correctness) {
        var row = '<tr>';
        if (names && names.length > 0) {
            $.each(names, function (index, name) {
                var s = item[name + ''];
                if(correctness[index] || correctness[index] === 0){
                    var c = 'no-correctness'
                    switch (correctness[index]){
                        case 0.5:
                            c = 'partial-right'
                            break;
                        case 0:
                            c  = 'wrong'
                            break;
                        case 1:
                            c = 'right'
                            break;
                    }
                    row += '<td id=' + c + '>' + c + ': ' + s + '</td>';
                } else {
                    row += '<td>' + s + '</td>';
                }

            });
        }
        row += '</tr>';
        return row;
    }

    /** Creates headers for the table. */
    function _setHeaders() {
        var h = '<tr>';
        if (_headers && _headers.length > 0) {
            $.each(_headers, function (index, header) {
                h += '<td>' + header + '</td>';
            });
        }
        h += '</tr>';
        if (_table.children('thead').length < 1) _table.prepend('<thead></thead>');
        _table.children('thead').html(h);
    }

    /** Set if there are no items guessed yet to compare*/
    function _setNoItemsInfo() {
        if (_table.length < 1) return; //not configured.
        var colspan = _headers != null && _headers.length > 0 ?
            'colspan="' + _headers.length + '"' : '';
        var content = '<tr class="no-items"><td ' + colspan + ' style="text-align:center">' +
            _defaultText + '</td></tr>';
        if (_table.children('tbody').length > 0)
            _table.children('tbody').html(content);
        else _table.append('<tbody>' + content + '</tbody>');
    }

    function _removeNoItemsInfo() {
        var c = _table.children('tbody').children('tr');
        if (c.length == 1 && c.hasClass('no-items')) _table.children('tbody').empty();
    }

    return {
        /** Configures the dynamic table. */
        config: function (tableId, fields, headers, defaultText) {
            _tableId = tableId;
            _table = $('#' + tableId);
            _fields = fields;
            _headers = headers;
            _defaultText = defaultText;
            _setHeaders();
            _setNoItemsInfo();
            return this;
        },
        /** Loads the specified data to the table body. */
        addGuess: function (data, correctness) {
            if (_table.length < 1) return; //not configured.
            _setHeaders();
            _removeNoItemsInfo();
            if (data) {
                var row = _buildCompareRowColumns(_fields, data, correctness);
                _table.children('tbody')['append'](row);
            } else {
                _setNoItemsInfo();
            }
            return this;
        }
    };
}());

// TODO: Parse CSV (temp)
// TODO: Look up (temp)
// TODO: select random pokemon
// TODO: use input when guessing
// TODO: compare selected and guess (Flask? or JS?)
$(document).ready(function(e) {

    var data1 = { 'Pokemon': 'Bulbasaur', 'Type I': 'Grass', 'Type II': 'Poison', 'Tier': 'NU', 'Egg Group I': 'Monster', 'Egg Group II': 'Grass', 'generation': '1', 'Evolve': '' };
    var correct1 = [1, 0.5, 0, 1, 1, 1, 0, 0.5, 1]

    var comparisons = compareTable.config('pokemon-compare-table',
        ['Pokemon', 'Type I', 'Type II', 'Tier', 'Egg Group I', 'Egg Group II', 'generation', 'Evolve'],
        ['Pokemon', 'Type I', 'Type II', 'Tier', 'Egg Group I', 'Egg Group II', 'Generation', 'Is Evolution'], //set to null for field names instead of custom header names
        'Guess a Pokemon First!');


    $('#btn-guess').click(function(e) {
        comparisons.addGuess(data1,correct1);
    });
});