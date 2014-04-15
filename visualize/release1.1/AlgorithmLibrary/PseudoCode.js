// Copyright 2011 David Galles, University of San Francisco. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without modification, are
// permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this list of
// conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice, this list
// of conditions and the following disclaimer in the documentation and/or other materials
// provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR IMPLIED
// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
// FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
// ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// The views and conclusions contained in the software and documentation are those of the
// authors and should not be interpreted as representing official policies, either expressed
// or implied, of the University of San Francisco



function PseudoCode(am, w, h)
{
	this.init(am, w, h);
}

PseudoCode.prototype = new Algorithm();
PseudoCode.prototype.constructor = PseudoCode;
PseudoCode.superclass = Algorithm.prototype;


// Various constants

var ANIMATOR_INITIAL_X = 20;
var ANIMATOR_INITIAL_Y = 20;

var LABEL_DATA_INSTANCE = 50;

var SINGLE_TYPE_HEIGHT = 50;

var ARRAY_TYPE_HEIGHT = 50;
var ARRAY_ELEM_WIDTH_SMALL = 30;
var ARRAY_ELEM_HEIGHT_SMALL = 30;

var TREE_ROOT_MIDDLE_X = 200;
var TREE_TYPE_HEIGHT = 50;
var TREE_TYPE_FLOOR_HEIGHT = 50;
var TREE_TYPE_FLOOR_WIDTH = 400;
var TREE_ELEM_WIDTH_SMALL = 30;
var TREE_ELEM_HEIGHT_SMALL = 30;
var TREE_TYPE_NODE_INTERVAL_WIDTH = 50;

var GRAPH_X_INTERVAL = 200;
var GRAPH_Y_INTERVAL = 100;
var SMALL_GRAPH_GROUP_SIZE = 5;
var GRAPH_TYPE_HEIGHT = 50;

var VERTEX_INDEX_COLOR = "#0000FF";
var EDGE_COLOR = "#007700";
var LINK_COLOR = "#007700";
var HIGHLIGHT_CIRCLE_COLOR = "#007700";
var FOREGROUND_COLOR = "#007700";
var BACKGROUND_COLOR = "EEFFEE";
var PRINT_COLOR = FOREGROUND_COLOR;

var SINGLE_TYPE = ['int', 'str', 'double', 'float', 'NoneType'];
var ARRAY_TYPE = ['list', 'tuple', 'dict', 'set', 'Stack', 'Queue'];
var TREE_TYPE = ['Tree', 'Node', 'BTree'];
var GRAPH_TYPE = ['Graph', 'DIGraph'];

var SPLITSTARTTOKEN = ['[', '{', '('];
var SPLITENDTOKEN = [']', '}', ')'];

PseudoCode.prototype.init = function(am, w, h)
{
	var sc = PseudoCode.superclass;
	var fn = sc.init;
	
	fn.call(this, am, w, h);
	this.addControls();
	this.nextIndex = 0;
	this.commands = [];
    this.pos_x = ANIMATOR_INITIAL_X;
    this.pos_y = ANIMATOR_INITIAL_Y;

	this.animationManager.StartNewAnimation(this.commands);
	this.animationManager.skipForward();
	this.animationManager.clearHistory();

    var t = this;
    setInterval(function(){t.implementAction(t.refresh.bind(t), "")}, 50);
}

PseudoCode.prototype.addControls =  function()
{
	this.insertField = addControlToAlgorithmBar("textarea", "", 160, 15);
    // this.insertField.onkeydown = this.returnSubmit(this.insertField, this.insertCallback.bind(this), 4);
	this.runButton = addControlToAlgorithmBar("Button", "Run");
	this.runButton.onclick = this.runCallback.bind(this);
}

PseudoCode.prototype.reset = function()
{
	this.nextIndex = 0;
    this.pos_x = ANIMATOR_INITIAL_X;
    this.pos_y = ANIMATOR_INITIAL_Y;
}

PseudoCode.prototype.runCallback = function(event)
{
	var pseudoCode = this.insertField.value;
	// Get text value
	// pseudoCode = this.normalizeNumber(insertedValue, 4);
	if (pseudoCode != "")
	{
		// set text value
		this.insertField.value = "";
		this.implementAction(this.run.bind(this), pseudoCode);
	}
}
		

PseudoCode.prototype.disableUI = function(event)
{
	//this.insertField.disabled = true;
	//this.runButton.disabled = true;
}

PseudoCode.prototype.enableUI = function(event)
{
	//this.insertField.disabled = false;
	//this.runButton.disabled = false;
}

PseudoCode.prototype.refresh = function()
{
    // read varlist from server
    this.clearAnimator();
    this.reset();

    // read file
    var xmldoc = readTextFile("varList.xml");
    
    var varList = xmldoc.getElementsByTagName("var");

    for (var i = 0; i < varList.length; i ++)
    {
        var varNode = varList[i].childNodes[0];
        var varInfo = [varList[i].getAttribute("name"),
                       varList[i].getAttribute("type"),
                       varNode.nodeValue]
        this.pos_x = ANIMATOR_INITIAL_X;
        this.plotVar(varInfo);
        console.log("Finish Plot : " + varInfo[0]);
    }

    this.animationManager.setAllLayers([0, this.currentLayer]);
	this.animationManager.StartNewAnimation(this.commands);
	this.animationManager.skipForward();
	this.animationManager.clearHistory();
    this.clearHistory();

}

PseudoCode.prototype.clearAnimator = function()
{
    this.commands = [];
    var alertMsg = "";
    for(var i = 0; i < this.nextIndex; i ++)
    {
        try
        {
            alertMsg = "Delete: " + String(i);
            console.log(alertMsg);
            this.cmd("Delete", i);
        }
        catch(err)
        {
            console.log("ID : " + i + " doesn't exist");
        }
    }
}
    
PseudoCode.prototype.plotVar = function(varInfo)
{
    // assert varInfo.length >= 3
    var alertMsg = ""
    var varName = varInfo[0].trim();
    var varType = varInfo[1].trim();

    if (SINGLE_TYPE.indexOf(varType) != -1)
    {
        varType = "SINGLE_TYPE";
    }
    else if (ARRAY_TYPE.indexOf(varType) != -1)
    {
        varType = "ARRAY_TYPE";
    }
    else if (TREE_TYPE.indexOf(varType) != -1)
    {
        varType = "TREE_TYPE";
    }
    else if (GRAPH_TYPE.indexOf(varType) != -1)
    {
        varType = "GRAPH_TYPE";
    }

    alertMsg = "CreateLabel: " + varName + ", Index: " + String(this.nextIndex);
    console.log(alertMsg);
    this.cmd("CreateLabel", this.nextIndex, varName, this.pos_x, this.pos_y);
    this.pos_x += LABEL_DATA_INSTANCE;
    this.nextIndex ++;
    if (varType == "SINGLE_TYPE")
    {
        var varValue = varInfo[2].trim().replace(/\'/g, "").replace(/\"/g, "");
        alertMsg = "CreateCircle: " + this.data + ", Index: " + String(this.nextIndex);
        // console.log(alertMsg);
        this.cmd("CreateCircle", this.nextIndex, varValue, this.pos_x, this.pos_y);
        this.pos_y += SINGLE_TYPE_HEIGHT;
        this.nextIndex ++;
    }
    else if (varType == "ARRAY_TYPE")
    {
        // var varValue = varInfo[2].slice(1, varInfo[2].length-1) 
        // remove '[' in first space and ']' in last space
        // varValue = varValue.split(", ")
        var strValue = varInfo[2];
        var arr = this.parseArray(strValue)
        for (var i = 0; i < arr.length; i ++)
        {
            alertMsg = "CreateRectangle: " + arr[i] + ", Index: " + String(this.nextIndex);
            // console.log(alertMsg);
            this.cmd("CreateRectangle", this.nextIndex, arr[i], ARRAY_ELEM_WIDTH_SMALL, ARRAY_ELEM_HEIGHT_SMALL, this.pos_x, this.pos_y);
            this.nextIndex ++;
            this.pos_x += ARRAY_ELEM_WIDTH_SMALL;
        }
        this.pos_y += ARRAY_TYPE_HEIGHT;
    }
    else if (varType == "TREE_TYPE")
    {
        //generate tree
        var strValue = varInfo[2];
        var tree = this.parseTree(strValue)
        // plot tree
        this.pos_x += TREE_ROOT_MIDDLE_X;
        this.plotTree(tree, 0, this.pos_x+TREE_ROOT_MIDDLE_X);
        this.pos_y += (tree.getHeight()-1) * TREE_TYPE_FLOOR_HEIGHT + TREE_TYPE_HEIGHT;
        console.log("Height : " + tree.getHeight());
    }
    else if (varType == "GRAPH_TYPE")
    {
        var strValue = varInfo[2];
        var graph = this.parseGraph(strValue);
        var max_y = this.plotGraph(graph);
        this.pos_y += max_y + GRAPH_TYPE_HEIGHT;
    }
    else
    {
        var errorMsg = "error!";
        for (var i = 0; i < varInfo.length; i ++)
        {
            errorMsg += varInfo[i] + " ";
        }
        alert(errorMsg);
    }
    return this.commands;
}


PseudoCode.prototype.parseArray = function(strValue)
{
    var optStack = [];
    var indx = 0;
    var arr = new Array();
    var token = "";
    while (indx < strValue.length)
    {
        var ch = strValue[indx];
        if (SPLITSTARTTOKEN.indexOf(ch) != -1)
        {
            optStack.push(ch);
            if (optStack.length > 1)
            {
                token += ch;
            }
        }
        else if (SPLITENDTOKEN.indexOf(ch) != -1)
        {
            var startToken = optStack.pop();
            if (SPLITSTARTTOKEN.indexOf(startToken) != SPLITENDTOKEN.indexOf(ch))
            {
                alert('Mismatch : ' + startToken + ' and ' + ch)
            }
            else
            {
                if (optStack.length >= 1)
                {
                    token += ch;
                }
                else
                {
                    arr.push(token.trim().replace(/\'/g, "").replace(/\"/g, ""));
                    token = "";
                }
            }
        }
        else if (ch == ',')
        {
            if (optStack.length > 1)
            {
                token += ch;
            }
            else
            {
                arr.push(token.trim().replace(/\'/g, "").replace(/\"/g, ""));
                token = "";
            }
        }
        else
        {
            token += ch;
        }
        indx ++;
    }
    // check if strVar is legal
    if (optStack.length != 0)
    {
        alert('var value illegal!');
    }
    alertMsg = "Get Array : " + arr.toString();
    console.log(alertMsg);

    return arr;
}



PseudoCode.prototype.parseTree = function(strValue)
{
    var optStack = [];
    var nodeStack = [];
    var tree = new Node();
    var token = "";
    // for (var indx = 0; indx < strValue.length; indx ++)
    var indx = 0;
    while (indx < strValue.length)
    {  
        var ch = strValue[indx];
        if (SPLITSTARTTOKEN.indexOf(ch) != -1)
        {
            // start of a node
            optStack.push(ch);
            token = "";
            ch = strValue[++indx];
            while(SPLITSTARTTOKEN.indexOf(ch) == -1 && SPLITENDTOKEN.indexOf(ch) == -1)
            {
                token += ch;
                ch = strValue[++indx];
            }
            var parentID = -1;
            if (nodeStack.length > 0)
            {
                parentID = nodeStack[nodeStack.length-1].getID();
            }
            if (token.trim() != "None")
            {
                token = token.trim().replace(/\'/g, "").replace(/\"/g, "");
                nodeStack.push(new Node(token, [], this.nextIndex, parentID));
                this.nextIndex ++;
            }
            else
            {
                token = token.trim().replace(/\'/g, "").replace(/\"/g, "");
                nodeStack.push(new Node(token, [], -1, parentID));
            }
        }
        else if (SPLITENDTOKEN.indexOf(ch) != -1)
        {
            // end of a node
            var startToken = optStack.pop();
            if (SPLITSTARTTOKEN.indexOf(startToken) != SPLITENDTOKEN.indexOf(ch))
            {
                alert('Mismatch : ' + startToken + ' and ' + ch)
            }
            else
            {
                if (optStack.length == 0)
                {
                    // last node in nodeStack, root node
                    tree = nodeStack.pop();
                }
                else
                {
                    // pop as subnode of prev node
                    var node = nodeStack.pop();
                    nodeStack[nodeStack.length-1].addChild(node);
                }
            }
            ++indx;
        }
        else
        {
            ++indx;
        }
    }
    // check if strVar is legal
    if ((nodeStack.length != 0) || (optStack.length != 0))
    {
        alert('var value illegal!');
    }
    alertMsg = "Get tree : " + tree.toString();
    console.log(alertMsg);

    return tree;
}


PseudoCode.prototype.parseGraph = function(strValue)
{
    var graph = new Graph();
    var vertexs = this.parseArray(strValue);
    for (var i = 0; i < vertexs.length; i ++)
    {
        var vertex = new Vertex();
        var tmp = this.parseArray(vertexs[i]);
        vertex.setValue(tmp[0]);
        vertex.setAdjs(this.parseArray(tmp[1]));
        vertex.setWeights(this.parseArray(tmp[2]));
        graph.addVertex(vertex);
    }
    return graph;
}


PseudoCode.prototype.plotTree = function(tree, level, pos_x)
{
    var pos_y = this.pos_y + level * TREE_TYPE_FLOOR_HEIGHT;
    if (tree.getParentID() == -1)
        // root node
    {
        this.cmd("CreateCircle", tree.objID, tree.value, pos_x, pos_y);
    }
    else
    {
         if (tree.getValue() != 'None')
         {
            this.cmd("CreateCircle", tree.objID, tree.value, pos_x, pos_y);
            this.cmd("Connect", 
                     tree.getParentID(), 
                     tree.objID, 
                     FOREGROUND_COLOR,
                     0, // curve
                     1, // directed
                     "", //label
                     0);
         }
    }
    level ++;
    var thisFloorWidth = TREE_TYPE_FLOOR_WIDTH * Math.pow(0.5, level-1);
    pos_x = pos_x - thisFloorWidth / 2;
    for (var i = 0; i < tree.children.length; i ++)
    {
        var node_x = pos_x 
        if (tree.children.length > 1)
        {
            node_x += i * thisFloorWidth / (tree.children.length-1);
        }
        this.plotTree(tree.children[i], level, node_x, pos_y);
    }
}
       

// plot graph
PseudoCode.prototype.plotGraph = function(graph, 
                                          showEdgeCosts=false, 
                                          directed=false)
{
    var size = graph.getSize();
    var circleID = new Array(size);
    var pos_logical = this.generateLogicalPos(size);
    var x_pos_logical = pos_logical[0];
    var y_pos_logical = pos_logical[1];
    var curve = pos_logical[2];
    var values = graph.getVertexValues();
    console.log(y_pos_logical);
    for (var i = 0; i < size; i ++)
    {
        circleID[i] = this.nextIndex ++;
        this.cmd("CreateCircle", circleID[i], values[i], this.pos_x + x_pos_logical[i], this.pos_y + y_pos_logical[i]);
        this.cmd("SetTextColor", circleID[i], VERTEX_INDEX_COLOR, 0);
        // this.cmd("SetLayer", circleID[i], 1);
    }
    var adj_matrix = graph.toMatrix();
    var adj_matrixID = new Array(size);
    for (var i = 0; i < size; i ++)
    {
        adj_matrixID[i] = new Array(size);
    }
    for (var i = 0; i < size; i ++)
    {
        for (var j = 0; j < size; j ++)
        {
            adj_matrixID[i][j] = this.index++;
        }
    }
    this.buildEdges(adj_matrix, x_pos_logical, y_pos_logical, curve, circleID, size, showEdgeCosts, directed);   
    return Math.max(y_pos_logical);
}


PseudoCode.prototype.generateLogicalPos = function(size)
{
    var x_pos_logical = new Array(size);
    var y_pos_logical = new Array(size);
    var curve = new Array(size);
    var group_size = 0;
    for (var i = 0; i < size; i++)
    {
        curve[i] = new Array(size);
    }
    if (size <= 10) // small size graph
    {
        group_size = SMALL_GRAPH_GROUP_SIZE;
    }
    else
    {
        group_size = Math.ceil(size / 2);
    }
    for (var i = 0; i < size; i++)
    {
        ingroup_index = i % group_size;
        group_index = Math.floor(i / group_size);
        x_pos_logical[i] = GRAPH_X_INTERVAL * 
                           ((ingroup_index % Math.ceil(group_size / 2)) + 
                             0.5 * Math.floor(ingroup_index / Math.ceil(group_size / 2)));
        y_pos_logical[i] = GRAPH_Y_INTERVAL * (2 * group_index + Math.floor(ingroup_index / Math.ceil(group_size / 2)));
        for (var j = 0; j < size; j ++)
        {
            if (group_index == Math.floor(j / group_size)) // i and j in same group, only consider in same line
            {
                if (Math.abs(i - j) >= 2 && 
                    Math.floor((i % group_size) / Math.ceil(group_size / 2)) == 
                    Math.floor((j % group_size) / Math.ceil(group_size / 2)))
                    // i and j in same line
                {
                    if (group_index < 1)
                    {
                        // curve up
                        curve[i][j] = 0.25 * Math.sign(i - j);
                    }
                    else
                    {
                        // curve down
                        curve[i][j] = 0.25 * Math.sign(j - 1);
                    }
                }
                else
                {
                    curve[i][j] = 0;
                }
            }
            // only have for columns, 2 groups, don't need to consider column curve
            else // don't consider italian case in this version
            {
                curve[i][j] = 0;
            }
        }
    }
    return [x_pos_logical, y_pos_logical, curve];
}


PseudoCode.prototype.buildEdges = function(adj_matrix, 
                                           x_pos_logical,
                                           y_pos_logical,
                                           curve, 
                                           circleID,
                                           size, 
                                           showEdgeCosts=true, 
                                           directed=false)
{
    for (var i = 0; i < size; i ++)
    {
        for (var j = 0; j < size; j++)
        {
            if (adj_matrix[i][j] >= 0)
            {
                var edgeLabel;
                if (showEdgeCosts)
                {
                    edgeLabel = String(this.adj_matrix[i][j]);
                }
                else
                {
                    edgeLabel = "";
                }
                if (directed)
                {
                    this.cmd("Connect", 
                             circleID[i], 
                             circleID[j], 
                             EDGE_COLOR, 
                             // this.adjustCurveForDirectedEdges([x_pos_logical[i], y_pos_logical[i]],
                             //                                  [x_pos_logical[j], y_pos_logical[j]],
                             //                                  adj_matrix),
                             0, 
                             1,
                             edgeLabel);
                }
                else if (i < j)
                {
                    this.cmd("Connect",
                             circleID[i],
                             circleID[j],
                             EDGE_COLOR,
                             curve[i][j], 
                             0,
                             edgeLabel);
                }
            }
        }
    }
}


// PseudoCode.prototype.adjustCurveForDirectedEdges(x_coordinate, y_coordinate, adj_matrix)
////////////////////////////////////////////////////////////
// Script to start up your function, called from the webapge:
////////////////////////////////////////////////////////////
var currentAlg;

function readTextFile(file)
{
    var xmlFile = new XMLHttpRequest();
    xmlFile.open("GET", file, false);
    // rawFile.open("GET", file, true);
    // rawFile.onreadystatechange = function()
    // {
    //     if (rawFile.readyState == 4)
    //     {
    //         if (rawFile.status == 200 || rawFile.status == 0)
    //         {
    //             varList = rawFile.responseText;
    //         }
    //     }
    // }
    xmlFile.send(null);
    var responsexml = xmlFile.responseXML;
    return responsexml
}

function init()
{
	var animManag = initCanvas();
	currentAlg = new PseudoCode(animManag, canvas.width, canvas.height);
}
