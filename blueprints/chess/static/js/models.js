
var Pieces = Backbone.Collection.extend({
    reset_moves: function(){
        _.each(this.models, function(m){
            m.set('moves', []);
        });
    }
});

var Piece = Backbone.Model.extend({
    image_prefix: '/chess/static/img',
    image_ext: 'png',
    image: 'Pawn',

    initialize: function(is_black) {
        this.is_black = !!is_black;
    },

    getImage: function() {
        return this.image_prefix + '/' + this.image + (this.get('is_black') ? 'B' : '') + '.' + this.image_ext;
    },

    addMove: function(move) {
        var moves = this.get('moves');
        moves.push(move);
    },

    canMoveTo: function(x, y) {
        var moves = this.get('moves');
        for (i in moves) {
            var m = moves[i]
            if (m[0] == x && m[1] == y) {
                return true
            }
        }
        return false;
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