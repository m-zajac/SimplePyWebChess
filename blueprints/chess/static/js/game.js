(function($){
    // pieces types dict
    types_dict = {
        'K': King,
        'Q': Queen,
        'b': Bishop,
        'k': Knight,
        'r': Rook,
        'p': Pawn
    }

    /**
     * Game object. Manages game, communicates with backend.
     */
    Game = function(){
        this.pieces = new Pieces;
        this.urls = {
            'init': 'chess/game/init',
            'move': 'chess/game/move'
        };
        this.game_data;
        this.black_moves = false;
    }

    Game.prototype = {
        /**
         * Prepare board (drags)
         */
        initBoard: function(){
            var g = this;
            var board_el = $('.game .board tbody');
            board_el.find('td').each(function(){
                $(this).droppable({
                    hoverClass: 'square-hover',
                    accept: function(draggable){
                        // accept only in td, and if there is a piece already - only if it's other players piece
                        //return $(this).is('td') && $(this).find('.piece[data-black="' + $(draggable[0]).attr('data-black') + '"]').length == 0;

                        var x = $(this).attr('data-x');
                        var y = $(this).attr('data-y');
                        var id = $(draggable[0]).attr('id');
                        var piece = g.pieces.get(id)
                        return piece.canMoveTo(x, y);
                    },
                    drop: function(event, ui) {
                        var dragged_piece_id = ui.draggable.first().attr('id');
                        var dragged_piece = g.pieces.get(dragged_piece_id);

                        var position = dragged_piece.get('position');
                        var destination = [
                            parseInt($(this).attr('data-x')),
                            parseInt($(this).attr('data-y')),
                        ];

                        // if there is other players piece, remove it
                        var captured_piece_el = $(this).find('.piece');
                        if (captured_piece_el.length > 0) {
                            var captured_piece_id = captured_piece_el.first().attr('id');
                            var captured_piece = g.pieces.get(captured_piece_id);

                            captured_piece.set('position', null);
                        }

                        dragged_piece.set('position', destination);

                        // move
                        g.move(position, destination);
                    }
                });
            });
            return this;
        },

        /**
         * Initialize pieces collection
         */
        initPieces: function() {
            this.pieces = new Pieces;
            return this;
        },

       /**
         * Initialize new game
         */
        setData: function(game_data){
            // capture containers
            whites_capture_cont = $('.game .white_captures');
            blacks_capture_cont = $('.game .black_captures');

            this.game_data = game_data;
            this.black_moves = game_data.game.black_moves;

            // create pieces from data
            _.each(game_data.game.board, this.updatePiece, this);
            _.each(game_data.game.white_captures, this.updatePiece, this);
            _.each(game_data.game.black_captures, this.updatePiece, this);
            
            // moves
            this.pieces.reset_moves();
            _.each(game_data.moves, function(move_data){
                id = move_data.pid
                piece = this.pieces.get(id)
                piece.addMove(move_data.to)
            }, this);

            return this;
        },

        updatePiece: function(piecedata){
            id = piecedata.id;
            piece = this.pieces.get(id);
            if (!piece) {
                piece = new types_dict[piecedata['t']];
                piece.set('id', id);
                piece.set('is_black', piecedata['b']);
                this.pieces.add(piece);

                view = new PieceView({
                    model: piece,
                    board: $('.game .board'),
                    capture_cont: (piece.get('is_black') ? whites_capture_cont : blacks_capture_cont)
                });
                view.render();
            }

            piece.set('position', piecedata['p']);
            piece.set('moves_count', piecedata['m']);
        },

        /**
         * Initialize new game
         */
        start: function(){
            var g = this;
            $.getJSON(this.urls.init, function(game_data) {
                g.setData(game_data);
            });

            return this;
        },

        move: function(position, destination){
            var g = this;
            $.post(
                this.urls.move, 
                JSON.stringify({
                    game_data: this.game_data,
                    move: [position, destination]
                }),
                function(game_data) {
                    g.setData(game_data);
                },
                'json'
            );

            return this;
        }
    }
})(jQuery)