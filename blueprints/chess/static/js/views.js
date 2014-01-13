(function($){

    PieceView = Backbone.View.extend({

        tagName: 'div',
        className: 'piece',

        initialize: function(options) {
            this.board = options.board;
            this.capture_cont = options.capture_cont;

            this.listenTo(this.model, 'change', this.update);

            // display moves on hover
            var g = this;
            this.$el.hover(
                function() {
                    _.forEach(g.model.getMovePositions(), function(move) {
                        $('.game .board td[data-x=' + move[0] + '][data-y=' + move[1] + ']').addClass('square-move-hint');
                    });
                }, 
                function() {
                    _.forEach(g.model.getMovePositions(), function(move) {
                        $('.game .board td[data-x=' + move[0] + '][data-y=' + move[1] + ']').removeClass('square-move-hint');
                    });
                }
            );
        },

        /**
         * Renders piece view
         */
        render: function() {
            // element
            this.$el.attr('id', this.model.get('id'));
            this.$el.attr('data-black', this.model.get('is_black'));
            this.$el.append(
                $('<img src="' + this.model.getImage() + '"/>')
            );

            // draggable
            this.$el.draggable({
                helper: 'clone'
            });

            // container
            var pos = this.model.get('position');
            if (pos) {
                $(this.board).find('td[data-x="' + pos[0] + '"][data-y="' + pos[1] + '"]').append(this.$el);
            } else {
                $(this.capture_cont).append(this.$el);
            }

            return this;
        },

        /**
         * Updates view
         */
        update: function() {
            var g = this;
            var pos = this.model.get('position');
            var captured = false;

            this.$el.attr('title', this.model.get('id') + ', ' + this.model.get('moves_count') + ' moves, pos: ' + this.model.get('position'));

            if (pos) {
                var dest = $(this.board).find('td[data-x="' + pos[0] + '"][data-y="' + pos[1] + '"]');
            } else {
                captured = true
                var dest = $(this.capture_cont);
            }

            var curr_parent = this.$el.parent();
            if (curr_parent[0] == dest[0]) {
                // no change
                return;
            }

            if (!captured && curr_parent[0] != this.capture_cont[0]) {
                var start_pos = this.$el.offset();
                var dest_pos = $(dest).offset();
                
                this.$el.css({
                    position: 'absolute',
                    left: this.$el.offset().left,
                    top: this.$el.offset().top,
                });
                dest.append(g.$el);
                this.$el.animate(
                    {
                        left: dest_pos.left,
                        top: dest_pos.top
                    }, {
                        duration: 500,
                        always: function(){
                            g.$el.css({
                                position: 'static'
                            });
                            g.$el.find('img').attr('src', g.model.getImage());
                        }
                    }
                );
            } else {
                dest.append(this.$el);
            }
        }
    });

    /**
     * Game view
     */
    GameView = function(game){
        this.game = game;
        var self = this;

        // ui events    
        $('#startgame').click(function(){
            self.game.start();
        });

        $('#starttest').click(function(){
            var game_url = $('#test_selector').val();
            self.game.start(game_url);
        });

        $('input[name=player_black_human]').click(function(){
            if ($(this).val() == 'true') {
                self.game.black_player_human = true;
            } else {
                self.game.black_player_human = false;
            }

            if (!self.game.black_player_human && self.game.black_moves) {
                self.game.move();
            }
        });
        $('input[name=player_black_human]:checked').trigger('click');

        $('input[name=player_white_human]').click(function(){
            if ($(this).val() == 'true') {
                self.game.white_player_human = true;
            } else {
                self.game.white_player_human = false;
            }

            if (!self.game.white_player_human && !self.game.black_moves) {
                self.game.move();
            }
        });
        $('input[name=player_white_human]:checked').trigger('click');

        // game events
        this.game.on('update', function(for_black){
            $('.player_marker.black, .player_marker.white').removeClass('checkmate check active');
            if (self.game.black_moves) {
                $('.player_marker.black').addClass('active');
            } else {
                $('.player_marker.white').addClass('active');
            }
        });
        this.game.on('check', function(for_black){
            if (for_black) {
                $('.player_marker.black').addClass('check');
            } else {
                $('.player_marker.white').addClass('check');
            }
        });
        this.game.on('checkmate', function(for_black){
            if (for_black) {
                $('.player_marker.black').addClass('checkmate');
            } else {
                $('.player_marker.white').addClass('checkmate');
            }
        });
    }
})(jQuery)