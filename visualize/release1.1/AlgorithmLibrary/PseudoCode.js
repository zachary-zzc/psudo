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
	//this.animationManager.StartNewAnimation(this.commands);
	//this.animationManager.skipForward();
	//this.animationManager.clearHistory();

    this.setup();
    // var id = window.setInterval(PseudoCode.prototype.refresh(curInfo), 100);
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
		

PseudoCode.prototype.run = function(pseudoCode)
{
    // call python function here
    // var xmlhttp;
    // if(window.XMLHttpRequest)
    // {// code for IE7+, Firefox, Chrome, Opera, Safari
    //     xmlhttp = new XMLHttpRequest();
    // }
    // else
    // {// code for IE6, IE5
    //     xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    // }
    // xmlhttp.onreadystatechange = function()
    // {
    //     if(xmlhttp.readyState==4 && xmlhttp.status==200)
    //     {
    //         // document.getElementById("Run").innerHTML = xmlhttp.responseText;
    //         alert(xmlhttp.responseText);
    //     }
    // }
    // xmlhttp.open("POST", "../../server.py", true);
    // xmlhttp.send(pseudoCode);*/
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

PseudoCode.prototype.setup = function()
{
    // read varlist from server
    // varLine format: varName, varType, varValue...
    //           e.g.: a, SingleType, 3,
    //               : b, ArrayType, 3, 4, 5, 6,

    // read file
    // var rawFile = new XMLHttpRequest();
    // rawFile.open("GET", "varList", false);
    // rawFile.send(null);
    // var varList = rawFile.responseText;
    // this.cmd("CreateLabel", 100, "help!", 100, 100);
    var varList = "a,SingleType,5";
    if (varList.indexOf("\n") >= 0)
    {
        var varLines = varList.split("\n");
    }
    else
    {
        var varLines = [varList];
    }

    for (var i = 0; i < varLines.length; i++)
    {
        var varInfo = varLines[i].split(",");
        var varName = varInfo[0];
        var varType = varInfo[1];
        if (varType == "SingleType")
        {
            var varValue = varInfo[2];
            this.singleTypeVar(varName, varValue);
            this.pos_y += SINGLE_TYPE_HEIGHT;
        }
        else if (varType == "ArrayType")
        {
            var varValue = new Array();
            for (var i = 2; i < varInfo.length; i++)
            {
                varValue.push(varInfo[i]);
            }
            this.arrayTypeVar(varName, varValue);
            this.pos_y += ARRAY_TYPE_HEIGHT;
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
            // alert("error!");
        }
        this.nextIndex ++;
    }
    this.animationManager.StartNewAnimation(this.commands);
    this.animationManager.skipForward();
    this.animationManager.clearHistory();
}

PseudoCode.prototype.clearAnimator = function()
{
    for(var i = this.nextIndex; i >= 0; i --)
    {
        this.cmd("Delete", i);
    }
    this.reset();
}
    

PseudoCode.prototype.singleTypeVar = function(varName, varValue)
{
    this.data = varValue;
    this.name = varName;

    this.cmd("CreateLabel", this.nextIndex, this.name, this.pos_x, this.pos_y);
    this.pos_x += LABEL_DATA_INSTANCE;
    this.nextIndex ++;
    this.cmd("CreateCircle", this.nextIndex, this.data, this.pos_x, this.pos_y);
}

PseudoCode.prototype.arrayTypeVar = function(varName, varValue)
{
    this.data = varValue;
    this.name - varName;

    this.cmd("CreateLabel", this.nextIndex, this.name, this.pos_x, this.pos_y);
    this.pos_x += LABEL_DATA_INSTANCE;
    this.nextIndex ++;

    for (var i = 0; i < this.data.length; i++)
    {
        this.cmd("CreateRectangle", this.nextIndex, this.data[i], ARRAY_ELEM_WIDTH_SMALL, ARRAY_ELEM_HEIGHT_SMALL, this.pos_x, this.pos_y);
        this.nextIndex ++;
        this.pos_x += ARRAY_ELEM_WIDTH_SMALL;
    }
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
