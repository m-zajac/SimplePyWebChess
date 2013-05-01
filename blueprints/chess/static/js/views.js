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
        var pos = this.model.get('position');
        if (pos) {
            $(this.board).find('td[data-x="' + pos[0] + '"][data-y="' + pos[1] + '"]').append(this.$el);
        } else {
            $(this.capture_cont).append(this.$el);
        }
    }
});