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
            var board_el = $('.game .board tbody');
            board_el.find('td').each(function(){
                $(this).droppable({
                    hoverClass: 'square-hover',
                    accept: function(draggable){
                        // accept only in td, and if there is a piece already - only if it's other players piece
                        return $(this).is('td') && $(this).find('.piece[data-black="' + $(draggable[0]).attr('data-black') + '"]').length == 0;
                    },
                    drop: function(event, ui) {
                        // if there is other players piece, remove it
                        var piece = $(this).find('.piece').first();
                        if (piece && piece.attr('data-black') != $(ui.draggable).attr('data-black')) {
                            piece.remove();
                        }

                        $(this).append(ui.draggable);
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

            // clear data
            if (this.pieces.models.length > 0) {
                _.each(this.pieces.models, function(el){
                    el.view.remove();
                });
                this.initPieces();
            }

            $.getJSON(this.urls.init, function(board_data) {
                var setup_color = function(data, is_black) {
                    for (id in data) {
                        piecedata = data[id]

                        piece = new types_dict[piecedata['t']];
                        piece.set('id', id);
                        piece.set('moves_count', piecedata['m']);
                        piece.set('is_black', is_black);

                        view = new PieceView({
                            model:      piece
                        });
                        piece.view = view;

                        view.render();
                        $('.game .board td[data-x="' + piecedata['p'][0] + '"][data-y="' + piecedata['p'][1] + '"]').append(view.$el);

                        g.pieces.add(piece);
                    }
                }
                setup_color(board_data.whites, false);
                setup_color(board_data.blacks, true);
            });

            return this;
        }
    }
})(jQuery)