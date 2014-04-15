// Data Structure 
// Tree
//------------------------------------------------------------------------------------------

function Node(value=null, children=[], objID=-1, parentID=-1)
{
    this.init(value, children, objID, parentID);
}

Node.prototype.init = function(value, children, objID, parentID)
{
    this.value = value;
    this.children = children;
    this.objID = objID;
    this.parentID = parentID;
}

Node.prototype.setValue = function(value)
{
    this.value = value;
}

Node.prototype.setChildren = function(children)
{
    this.children = children;
}

Node.prototype.setChild = function(child, indx)
{
    this.children[indx] = child;
}

Node.prototype.setID = function(objID)
{
    this.objID = objID;
}

Node.prototype.setParentID = function(parentID)
{
    this.parentID = objID;
}

Node.prototype.addChild = function(child)
{
    this.children.push(child)
}

Node.prototype.getValue = function()
{
    return this.value;
}

Node.prototype.getChildren = function()
{
    return this.children;
}

Node.prototype.getChild = function(indx)
{
    return this.children[indx];
}

Node.prototype.getID = function()
{
    return this.objID;
}

Node.prototype.getParentID = function()
{
    return this.parentID;
}

Node.prototype.getHeight = function()
{
    if (this.children.length == 0)
    {
        return 1;
    }
    var childHeight = new Array(this.children.length);
    for (var i = 0; i < this.children.length; i ++)
    {
        childHeight[i] = this.children[i].getHeight();
    }
    // console.log(Math.max.apply(null, childHeight) + 1);
    return Math.max.apply(null, childHeight) + 1;
}

Node.prototype.toString = function()
{
    var ret = '[' + this.value;
    for (var i = 0; i < this.children.length; i ++)
    {
        ret += this.children[i].toString();
    }
    ret += ']';
    return ret;
}
