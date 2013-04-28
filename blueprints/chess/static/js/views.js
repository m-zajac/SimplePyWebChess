var PieceView = Backbone.View.extend({

    tagName: 'div',
    className: 'piece',

    initialize: function() {
        
    },

    render: function() {
        this.$el.attr('data-black', this.model.get('is_black'));
        this.$el.append(
            $('<img src="' + this.model.getImage() + '"/>')
        );

        this.$el.draggable({
            helper: 'clone'
        });

        return this;
    }
});