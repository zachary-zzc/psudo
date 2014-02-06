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

PseudoCode.HIGHLIGHT_LABEL_COLOR = "#FF0000"
PseudoCode.HIGHLIGHT_LINK_COLOR = "#0FF0000"

PseudoCode.HIGHLIGHT_COLOR = "#007700"
PseudoCode.HEIGHT_LABEL_COLOR = "#0x00AA00"


PseudoCode.LINK_COLOR = "#007700";
PseudoCode.HIGHLIGHT_CIRCLE_COLOR = "#007700";
PseudoCode.FOREGROUND_COLOR = "0x007700";
PseudoCode.BACKGROUND_COLOR = "#DDFFDD";
PseudoCode.PRINT_COLOR = PseudoCode.FOREGROUND_COLOR;

PseudoCode.WIDTH_DELTA  = 50;
PseudoCode.HEIGHT_DELTA = 50;
PseudoCode.STARTING_Y = 50;

PseudoCode.FIRST_PRINT_POS_X  = 50;
PseudoCode.PRINT_VERTICAL_GAP  = 20;
PseudoCode.PRINT_HORIZONTAL_GAP = 50;
PseudoCode.EXPLANITORY_TEXT_X = 10;
PseudoCode.EXPLANITORY_TEXT_Y = 10;



PseudoCode.prototype.init = function(am, w, h)
{
	var sc = PseudoCode.superclass;
	var fn = sc.init;
	this.first_print_pos_y  = h - 2 * PseudoCode.PRINT_VERTICAL_GAP;
	this.print_max = w - 10;
	
	fn.call(this, am, w, h);
	this.startingX = w / 2;
	this.addControls();
	this.nextIndex = 1;
	this.commands = [];
	this.cmd("CreateLabel", 0, "", PseudoCode.EXPLANITORY_TEXT_X, PseudoCode.EXPLANITORY_TEXT_Y, 0);
	this.animationManager.StartNewAnimation(this.commands);
	this.animationManager.skipForward();
	this.animationManager.clearHistory();
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
	this.nextIndex = 1;
	//this.treeRoot = null;
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
		
PseudoCode.prototype.refresh = function()
{
    // this function response to python compiler execution call
	return this.commands;
}

PseudoCode.prototype.run = function(pseudoCode)
{
    // call python function here
    var xmlhttp;
    if(window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function()
    {
        if(xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            // document.getElementById("Run").innerHTML = xmlhttp.responseText;
            alert(xmlhttp.responseText);
        }
    }
    xmlhttp.open("POST", "../../server.py", true);
    xmlhttp.send(pseudoCode);
}

PseudoCode.prototype.disableUI = function(event)
{
	this.insertField.disabled = true;
	this.runButton.disabled = true;
}

PseudoCode.prototype.enableUI = function(event)
{
	this.insertField.disabled = false;
	this.runButton.disabled = false;
}

		
/*function PseudoCodeNode(val, id, hid, initialX, initialY)
{
	this.data = val;
	this.x = initialX;
	this.y = initialY;
	this.heightLabelID= hid;
	this.height = 1;
	
	this.graphicID = id;
	this.left = null;
	this.right = null;
	this.parent = null;
}*/

function info(initialID, initialX, initialY)
{
    this.id = initialID;
    this.x = initialX;
    this.y = initialY;
}

function Refresh(curInfo, varList)
{
    this.curInfo = clearAnimator(curInfo); 
    // read varlist from server
    // varLine format: varName, varType, varValue...
    //           e.g.: a, SingleType, 3,
    //               : b, ArrayType, 3, 4, 5, 6,
    var varLines = varList.split("\n");
    for (var i = 0; i < varLines.length; i++)
    {
        var varInfo = varLines[i].split(",");
        var varName = varInfo[0];
        var varType = varInfo[1];
        if (varType == "SingleType")
        {
            var varValue = varInfo[2];
            this.curInfo = SingleTypeVar(varName, varValue, this.curInfo);
            this.curInfo.y += SINGLE_TYPE_HEIGHT;
        }
        else if (varType == "ArrayType")
        {
            var varValue = new Array();
            for (var i = 2; i < varInfo.length; i++)
            {
                varValue.push(varInfo[i]);
            }
            this.curInfo = ArrayTypeVar(varName, varValue, this.curInfo);
            this.curInfo.y += ARRAY_TYPE_HEIGHT;
        }
        // else if (varType == "TreeType")
        // {
        // }
        // else if (varType == "GraphType")
        // {
        // }
        // else if (varType == "DiGraphType")
        // {
        // }
        else
        {
            alert("error!");
        }
        this.curInfo.id += 1;
    }
}

function clearAnimator(curInfo)
{
    this.curInfo = new info(curInfo.id, ANIMATOR_INITIAL_X, ANIMATOR_INITIAL_Y);
    for(this.curInfo.id; this.curIndo.id >= 0; this.curInfo.id --)
    {
        this.cmd("Delete", this.curInfo.id);
    }
    return this.curInfo;
}
    

function SingleTypeVar(varName, varValue, curInfo)
{
   this.data = varValue;
   this.name = varName;
   this.curInfo = new info(curInfo.id, curInfo.x, curInfo.y);

   this.cmd("CreateLabel", this.curInfo.id, this.name, this.curInfo.x, this.curInfo.y);
   this.curInfo.x += LABEL_DATA_INSTANCE;
   this.curInfo.id += 1;
   this.cmd("CreateCircle", this.id, this.data, this.x, this.y);
   
   return this.curInfo;
}

function ArrayTypeVar(varName, varValue, curInfo)
{
    this.data = varValue;
    this.name - varName;
    this.curInfo = new info(curInfo.id, curInfo.x, curInfo.y);

    this.cmd("CreateLabel", this.curInfo.id, this.name, this.curInfo.x, this.curInfo.y);
    this.curInfo.x += LABEL_DATA_INSTANCE;
    this.curInfo.id += 1;

    for (var i = 0; i < this.data.length; i++)
    {
        this.cmd("CreateRectangle", this.curInfo.id, this.data[i], ARRAY_ELEM_WIDTH_SMALL, ARRAY_ELEM_HEIGHT_SMALL, this.curInfo.x, this.curInfo.y);
        this.curInfo.id += 1;
        this.curInfo.x += ARRAY_ELEM_WIDTH_SMALL;
    }

    return this.curInfo;
}

/*
function TreeTypeVar()
{

}

function GraphTypeVar()
{

}

function DiGraphTypeVar()
{

}*/

////////////////////////////////////////////////////////////
// Script to start up your function, called from the webapge:
////////////////////////////////////////////////////////////
var currentAlg;

function init()
{
	var animManag = initCanvas();
	currentAlg = new PseudoCode(animManag, canvas.width, canvas.height);
}
