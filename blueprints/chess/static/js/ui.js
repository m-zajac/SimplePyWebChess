$(function(){
    // init board
    var board_container = $('.game .board');
    var board_table = $('<table/>');
    var board_body = $('<tbody/>');
    for (var i = 7; i >= 0; i--) {
        var row = $('<tr/>');
        for (var j = 0; j < 8; j++) {
            row.append($('<td data-x="' + j + '" data-y="' + i + '"/>'));
        }
        board_body.append(row);
    }
    board_table.append(board_body);
    board_container.append(board_table);

    // init game
    var game = new Game();
    game.initBoard();
    game.initPieces();

    // events    
    $('#startgame').click(function(){
        game.start();
    })
})