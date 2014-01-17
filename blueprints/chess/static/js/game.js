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
        //Backbone events - for view
        _.extend(this, Backbone.Events);

        this.pieces = new Pieces;
        this.urls = {
            'init': 'chess/game/init',
            'move': 'chess/game/move'
        };
        this.game_data;

        // game state
        this.black_moves = false;
        this.white_player_human = true;
        this.black_player_human = true;
        this.is_check = false;
        this.is_checkmate = false;
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

                        var moves = dragged_piece.getMovesByTarget(destination)
                        var move;

                        if (moves.length > 1) {
                            g.chooseMove(dragged_piece, moves);
                            return;
                        } else if (moves.length > 0) {
                            move = moves[0];
                        }

                        if (!move) {
                            return;
                        }

                        var move = moves[0];

                        // if there is other players piece, remove it
                        var captured_piece_el = $(this).find('.piece');
                        if (captured_piece_el.length > 0) {
                            var captured_piece_id = captured_piece_el.first().attr('id');
                            var captured_piece = g.pieces.get(captured_piece_id);

                            captured_piece.set('position', null);
                        }

                        dragged_piece.set('position', destination);

                        // move
                        g.move(move);
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
            this.is_check = game_data.game.is_check;
            this.is_checkmate = game_data.game.is_checkmate;

            // create pieces from data
            _.each(game_data.game.board, this.updatePiece, this);
            _.each(game_data.game.white_captures, this.updatePiece, this);
            _.each(game_data.game.black_captures, this.updatePiece, this);

            // moves
            this.pieces.reset_moves();
            _.each(game_data.moves, function(move_data){
                id = move_data.pid
                piece = this.pieces.get(id)
                piece.addMove(move_data.move)
            }, this);

            // trigger events
            this.trigger('update');

            if (this.is_check && !this.is_checkmate) {
                this.trigger('check', this.black_moves);
            } else if (this.is_check && this.is_checkmate) {
                this.trigger('checkmate', this.black_moves);
            } else if (!this.is_check && this.is_checkmate) {
                this.trigger('stalemate', this.black_moves);
            }

            return this;
        },

        updatePiece: function(piecedata){
            id = piecedata.id;
            piece = this.pieces.get(id);
            if (!piece) {
                piece = new types_dict[piecedata['t']];
                piece.set('id', id);
                piece.set('is_black', piecedata['b']);
                piece.type = piecedata['t'];
                this.pieces.add(piece);

                view = new PieceView({
                    model: piece,
                    board: $('.game .board'),
                    capture_cont: (piece.get('is_black') ? whites_capture_cont : blacks_capture_cont)
                });
                piece.view = view;
                view.render();
            } else if (piece.type != piecedata['t']) {
                var new_type_piece = new types_dict[piecedata['t']];
                piece.type = new_type_piece.type;
                piece.image = new_type_piece.image;
                piece.view.update();
            }

            piece.set('position', piecedata['p']);
            piece.set('moves_count', piecedata['m']);
        },

        /**
         * Initialize new game
         */
        start: function(url){
            if (!url) {
                url = this.urls.init;
            }

            var g = this;
            $.post(
                url, 
                this._prepare_post_data(),
                function(game_data) {
                    g.setData(game_data);
                }
            );

            return this;
        },

        move: function(move) {
            var g = this;
            var data = null;
            if (move) {
                data = this._prepare_post_data(move);
            } else {
                data = this._prepare_post_data();
            }

            $.post(
                this.urls.move,
                data,
                function(game_data) {
                    g.setData(game_data);

                    // computer move
                    if (
                        (g.black_moves && !g.black_player_human)
                        ||
                        (!g.black_moves && !g.white_player_human)
                    ) {
                        if (!g.is_checkmate) {
                            setTimeout(function(){
                                g.move();
                            }, 1000 );
                        }
                    }
                },
                'json'
            );
            return this;
        },

        chooseMove: function(piece, moves) {
            var g = this;
            var dialog = $('<div class="modal fade" style="width: 135px;"/>');
            var dialog_header = $('<div class="modal-header"><button type="button" class="close" data-dismiss="modal">×</button><h3 id="myModalLabel">Choose piece</h3>');
            var dialog_body = $('<div class="modal-body"/>');
            var dialog_buttons = $('<div class="modal-footer"><button class="btn btn-inverse" data-dismiss="modal">Cancel</button>');
            for (var i in moves) {
                var new_p_class = types_dict[moves[i]['tt']]
                if (!new_p_class) {
                    continue;
                }

                var new_p = new new_p_class;
                new_p.set('is_black', piece.get('is_black'));
                var new_p_img = new_p.getImage();
                var new_p_container = $('<div class="piece"/>');
                new_p_container.append('<img src="' + new_p_img + '" alt=""/>');

                var create_click_event = function(move){
                    return function(){
                        dialog.modal('hide');
                        g.move(move);
                    };
                }
                new_p_container.click(create_click_event(moves[i]));

                dialog_body.append(new_p_container);
            }

            dialog.append(dialog_body).append(dialog_buttons).modal('show');
        },

        _prepare_post_data: function(move) {
            return JSON.stringify({
                game_data: this.game_data,
                move: move
            });
        }
    }
})(jQuery)