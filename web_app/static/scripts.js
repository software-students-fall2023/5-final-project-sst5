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
                if(name === 'TypeTwo' && s === '') s = 'None';
                if(name === 'EgTwo' && s === '') s = 'None';
                if(name === 'Evo' && s === '') s = 'Not an Evolution';
                if(correctness[index] || correctness[index] === false){
                    var c = 'no-correctness'
                    switch (correctness[index]){
                        case false:
                            c  = 'wrong'
                            break;
                        case true:
                            c = 'right'
                            break;
                    }
                    row += '<td id=' + c + '>' +  s + '</td>';
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
        if (c.length === 1 && c.hasClass('no-items')) _table.children('tbody').empty();
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

function checkWin(correctness){
    var win = true;
    for(var i = 0; i < correctness.length; i++){
        if(correctness[i] !== true) win = false;
    }
    return win;
}

let comparisons, fields;

function getCorrectness(data){
    var correctness = []
    if(fields){
        for(var i = 0; i < fields.length; i++){
            var key = 'is'+fields[i];
            correctness.push(data[key]);
        }
        return correctness;
    }
}
$(document).ready(function(e) {

    fields = ['Pokemon', 'TypeOne', 'TypeTwo', 'Tier', 'EgOne', 'EgTwo', 'Generation', 'Evo'];

    comparisons = compareTable.config('pokemon-compare-table',
        fields,
        ['Pokemon', 'Type I', 'Type II', 'Tier', 'Egg Group I', 'Egg Group II', 'Generation', 'Is Evolution'], //set to null for field names instead of custom header names
        'Guess a Pokemon First!');
});