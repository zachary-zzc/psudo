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

// Data Structure 
// Tree
//------------------------------------------------------------------------------------------

/*function Node()
{

}

Node.prototype.init = function(value, children=[])
{
    this.value = value;
    this.children = children;
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

Node.prototype.getValue = function()
{
    return this.value;
}

Node.prototype.getChildren = function(indx=null)
{
    if (indx === null)
    {
        return this.children;
    }
    else
    {
        return this.children[indx];
    }
}

function Tree(value=null, children=[])
{
    this.init(value, children)
}

Tree.prototype = new Node();
Tree.prototype.constructor = Tree;
Tree.superclass = Node.prototype;

Tree.prototype.init(value, children)
{
   var sc = Tree.superclass;
   var fn = sc.init;
   fn.call(this, value, children)
}

Tree.prototype.preorderTraversal(func)
{

}

Tree.prototype.inorderTraversal(func)
{

}

Tree.prototype.postorderTraversal(func)
{

}*/

//------------------------------------------------------------------------------------------

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

var SINGLE_TYPE_HEIGHT = 50;
var ARRAY_TYPE_HEIGHT = 50;

var LABEL_DATA_INSTANCE = 30;

var ARRAY_ELEM_WIDTH_SMALL = 30;
var ARRAY_ELEM_HEIGHT_SMALL = 30;

var SINGLE_TYPE = ['int', 'str', 'double', 'float']
var ARRAY_TYPE = ['list', 'tuple', 'dict', 'set', 'Stack', 'Queue']
var TREE_TYPE = ['Tree']
// Global Variable
varList = ""

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

    // this.implementAction(this.refresh.bind(this), "");
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
    this.commands = [];
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
    // varLine format: varName, varType, varValue...
    //           e.g.: a, SingleType, 3,
    //               : b, ArrayType, 3, 4, 5, 6,

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
    }
    return this.commands;
}

PseudoCode.prototype.clearAnimator = function()
{
    var tmpIndex = this.nextIndex;
    this.reset();
    var alertMsg = "";
    for(var i = 0; i < tmpIndex; i ++)
    {
        alertMsg = "Delete: " + String(i);
        //console.log(alertMsg);
        this.cmd("Delete", i);
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
    else if (DIGRAPH_TYPE.indexOf(varType) != -1)
    {
        varType = "DIGRAPH_TYPE";
    }

    alertMsg = "CreateLabel: " + varName + ", Index: " + String(this.nextIndex);
    console.log(alertMsg);
    this.cmd("CreateLabel", this.nextIndex, varName, this.pos_x, this.pos_y);
    this.pos_x += LABEL_DATA_INSTANCE;
    this.nextIndex ++;
    if (varType == "SINGLE_TYPE")
    {
        var varValue = varInfo[2].trim();
        alertMsg = "CreateCircle: " + this.data + ", Index: " + String(this.nextIndex);
        console.log(alertMsg);
        this.cmd("CreateCircle", this.nextIndex, varValue, this.pos_x, this.pos_y);
        this.pos_y += SINGLE_TYPE_HEIGHT;
        this.nextIndex ++;
    }
    else if (varType == "ARRAY_TYPE")
    {
        var varValue = varInfo[2].slice(1, varInfo[2].length-2) // remove '[' in first space and ']' in last space
        varValue = varValue.split(", ")
        for (var i = 0; i < varValue.length; i ++)
        {
            alertMsg = "CreateRectangle: " + varValue[i] + ", Index: " + String(this.nextIndex);
            //console.log(alertMsg);
            this.cmd("CreateRectangle", this.nextIndex, varValue[i], ARRAY_ELEM_WIDTH_SMALL, ARRAY_ELEM_HEIGHT_SMALL, this.pos_x, this.pos_y);
            this.nextIndex ++;
            this.pos_x += ARRAY_ELEM_WIDTH_SMALL;
        }
        this.pos_y += ARRAY_TYPE_HEIGHT;
    }
    /*
    else if (this.varType == "TreeType")
    {
    }
    /*
    else if (this.varType == "GraphType")
    {
    }
    else if (this.varType == "DiGraphType")
    {
    }*/
    else
    {
        var errorMsg = "error!";
        for (var i = 0; i < varInfo.length; i ++)
        {
            errorMsg += varInfo[i] + " ";
        }
        alert(errorMsg);
    }
}


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
