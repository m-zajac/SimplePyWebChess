var PieceView = Backbone.View.extend({

    tagName: 'div',
    className: 'piece',

    initialize: function(options) {
        this.board = options.board;
        this.capture_cont = options.capture_cont;

        this.listenTo(this.model, 'change', this.updatePosition);
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
     * Updates piece position
     */
    updatePosition: function() {
        var g = this;
        var pos = this.model.get('position');
        var capture = false;

        if (pos) {
            var dest = $(this.board).find('td[data-x="' + pos[0] + '"][data-y="' + pos[1] + '"]');
        } else {
            capture = true
            var dest = $(this.capture_cont);
        }

        var curr_parent = this.$el.parent();
        if (curr_parent[0] == dest[0]) {
            // no change
            return;
        }

        if (!capture && curr_parent[0] != this.capture_cont[0]) {
            var start_pos = this.$el.offset();
            var dest_pos = $(dest).offset();
            console.log(this.model.get('is_black'), start_pos, dest_pos, curr_parent)
            this.$el.css({
                position: 'absolute',
                left: this.$el.offset().left,
                top: this.$el.offset().top,
            });
            this.$el.animate(
                {
                    left: dest_pos.left,
                    top: dest_pos.top
                }, 
                500, 
                function(){
                    dest.append(g.$el);
                    g.$el.css({
                        position: 'static'
                    });
                }
            );
        } else {
            dest.append(this.$el);
        }
    }
});