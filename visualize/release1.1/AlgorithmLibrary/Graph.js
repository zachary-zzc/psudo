// Data Structure 
// Graph
//------------------------------------------------------------------------------------------

function Vertex(value=null, adjs=[], weights=[])
{
    this.init(value, adjs, weights);
}


Vertex.prototype.init = function(value, adjs, weights)
{
    this.value = value;
    this.adjs = adjs;
    this.weights = weights;
}


Vertex.prototype.getValue = function()
{
    return this.value;
}


Vertex.prototype.setValue = function(value)
{
    this.value = value;
}


Vertex.prototype.getAdjs = function()
{
    return this.adjs;
}


Vertex.prototype.setAdjs = function(adjs)
{
    this.adjs = adjs;
}


Vertex.prototype.getWeights = function()
{
    return this.weights;
}


Vertex.prototype.setWeights = function(weights)
{
    this.weights = weights;
}


Vertex.prototype.toString = function()
{
    var ret = [this.value, this.adjs, this.weights];
    return ret.toString();
}


function Graph(vertexs = [])
{
    this.init(vertexs);
}


Graph.prototype.init = function(vertexs)
{
    this.vertexs = vertexs;
}


Graph.prototype.getVertexs = function()
{
    return this.vertexs;
}


Graph.prototype.getVertexValues = function()
{
    var values = new Array(this.vertexs.length);
    for (var i = 0; i < this.vertexs.length; i ++)
    {
        values[i] = this.vertexs[i].getValue();
    }
    return values;
}


Graph.prototype.setVertexs = function(vertexs)
{
    this.vertexs = vertexs;
}


Graph.prototype.addVertex = function(vertex)
{
    this.vertexs.push(vertex);
}


Graph.prototype.getSize = function()
{
    return this.vertexs.length;
}



Graph.prototype.toString = function()
{
    return this.vertexs.toString();
}


Graph.prototype.toMatrix = function()
{
    // init adj_matrix
    var adj_matrix = new Array(this.vertexs.length);
    var vertexList = [];
    for (var i = 0; i < this.vertexs.length; i ++)
    {
        adj_matrix[i] = new Array(this.vertexs.length);
        vertexList.push(this.vertexs[i].getValue());
    }
    for (var i = 0; i < this.vertexs.length; i ++)
    {
        for (var j = 0; j < this.vertexs.length; j ++)
        {
            adj_matrix[i][j] = -1;
        }
    }
    // generate adj_matrix
    for (var i = 0; i < this.vertexs.length; i ++)
    {
        var adjs = this.vertexs[i].getAdjs();
        var weights = this.vertexs[i].getWeights();
        for (var j = 0; j < adjs.length; j ++)
        {
            var x_indx = vertexList.indexOf(this.vertexs[i].getValue());
            var y_indx = vertexList.indexOf(adjs[j]);
            adj_matrix[x_indx][y_indx] = weights[j];
        }
    }
    
    return adj_matrix;
}

//------------------------------------------------------------------------------------------

