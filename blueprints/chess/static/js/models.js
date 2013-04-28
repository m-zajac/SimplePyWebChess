
var Piece = Backbone.Model.extend({
    image_prefix: '/chess/static/img',
    image_ext: 'png',
    image: 'Pawn',

    initialize: function(is_black) {
        this.is_black = !!is_black;
    },

    getImage: function() {
        return this.image_prefix + '/' + this.image + (this.get('is_black') ? 'B' : '') + '.' + this.image_ext;
    }
});

var King = Piece.extend({
    image: 'King'
});

var Queen = Piece.extend({
    image: 'Queen'
});

var Rook = Piece.extend({
    image: 'Rook'
});

var Knight = Piece.extend({
    image: 'Knight'
});

var Bishop = Piece.extend({
    image: 'Bishop'
});

var Pawn = Piece.extend({
    image: 'Pawn'
});