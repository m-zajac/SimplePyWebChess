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
        this.pieces = new Backbone.Collection;
        this.urls = {
            'init': 'chess/game/init'
        }
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
                        return $(this).is('td') && $(this).find('.piece[data-black="' + $(draggable[0]).attr('data-black') + '"]').length == 0;
                    },
                    drop: function(event, ui) {
                        var dragged_piece_id = ui.draggable.first().attr('id');
                        var dragged_piece = g.pieces.get(dragged_piece_id);

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
                    }
                });
            });
            return this;
        },

        /**
         * Initialize pieces collection
         */
        initPieces: function() {
            this.pieces = new Backbone.Collection;
            return this;
        },

        /**
         * Initialize new game
         */
        start: function(){
            var g = this;

            $.getJSON(this.urls.init, function(board_data) {
                // capture containers
                whites_capture_cont = $('.game .white_captures');
                blacks_capture_cont = $('.game .black_captures');

                // create pieces from data
                for (id in board_data) {
                    piecedata = board_data[id];
                    piece = g.pieces.get(id);
                    if (!piece) {
                        piece = new types_dict[piecedata['t']];
                        piece.set('id', id);
                        piece.set('is_black', piecedata['b']);

                        g.pieces.add(piece);

                        view = new PieceView({
                            model: piece,
                            board: $('.game .board'),
                            capture_cont: (piece.get('is_black') ? whites_capture_cont : blacks_capture_cont)
                        });
                        view.render();
                    }

                    piece.set('position', piecedata['p']);
                    piece.set('moves_count', piecedata['m']);
                }
            });

            return this;
        }
    }
})(jQuery)