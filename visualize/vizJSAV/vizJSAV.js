var av;

$(document).ready(
 $.getJSON('json_temp.json', readJsonFile(data));
);

function readJsonFile(data){
    var variable;
    for (var i =0; i<data.length; i++){
        variable = data[i].Vars; 
        if (variable != null){
            vizJSAV.pr.plotVar(variable);
        }
    }
}


function vizJSAV(am, w, h){
	this.init(am, w, h);
	av.umsg("Ready!", {"color": "blue"});
 //   vizJSAV.prototype.refresh(); 
}

vizJSAV.prototype.setCSS=function(obj,cssStr){
    obj.css(cssStr);
}
//indices is a list of elements to be highligted[1.2,3]
vizJSAV.prototype.arrayHighlight(array, indices){
    array.highlight(indices);
}
vizJSAV.prototype.arrayUnhighlight(array, indices){
    array.unhighlight(indices);
}
vizJSAV.prototype.linkedListHighlight(linkedList, index){
    linkedList.get(index).highlight();
}
vizJSAV.prototype.linkedListUnhighlight(linkedList, index){
    linkedList.get(index).unhighlight();
}

vizJSAV.prototype.plotVar = function(variable){
/*
    var varName = varInfo[0].trim();
    var varType = varInfo[1].trim(); 
    var varValueStr = varInfo[2].trim();
*/
    var varType = variable.type; 

    var varValue;
    var avVar;
    switch (varType){
        case "int": 
            varValue = variable.value;
            break;
        case "list": 
            varValue = this.parseList(variable);
            avVar= av.ds.array(avValue);
            break;
        case "stack": 
            varValue = this.parseStack(variable);
            avVar=av.ds.array(varValue);
            break;
        case "matrix": 
            varValue = this.parseMatrix(variable);
            avVar=av.ds.matrix(varValue);
            break;

        case "BTree": 
            avVar=this.parseBTree(variable);
            break;
        case "Graph": 
            avVar = this.parseGraph(variable);
            break;
        case "linkedList":
            avVar = this.parseLinkedList(variable);
        default: break;
    }
}



vizJSAV.prototype.parseList=function(variable){
	var list = new array();
	var len = variable["length"];
    var valueStr = variable["value"];
	if (valueStr[0]=='(' && valueStr[len-1]==')' && valueStr.length == (2*len+1)){
		valueStr = value.substr(1, varValueStr.length-2);
	}else{
		alert("Invalid input! \n");
	}
    var valueCharList = value.split(',');
    for (var i=0; i<len; i++){
        list.push(parseInt(valueCharList[i]));
    }
}

vizJSAV.prototype.parseStack=function(variable){
	var isEmpty =  attrs.getNamedItem("isEmpty");
	if (isEmpty)
		alert("Invalid input! \n");
	else
		return this.parseList(variable);
}

vizJSAV.prototype.parseMatrix=function(variable){
	var matrixStr=variable["value"].substr(1, str.len-2);
	var nCols=variable["n_cols"];
	var nRows=variable["n_rows"];
	var rows = matrixStr.split(']');
    rows=rows.join('').split('');
	var matrix = new array();
	if (rows.length!= nRows){		
		alert("Invalid input! \n");
		return;
	}else{
		for (var i=0; i<nRows;i++){

            rows[i].replace('[','');
			var rowsCharList = rows[i].split(',');
			rowsCharList=rowsCharList.join('').split('');//remove empty cells
			if (rowsCharList.length!=nCols){				
				alert("Invalid input! \n");
				return;
			}

            var tempRow = new array();
            for (var j=0; j<rowsCharList.length;j++){
                tempRow.push(parseInt(rowsCharList[j]));
            } 
                
			matrix.push(tempRow);
		}
		return matrix;
	}
}

vizJSAV.prototype.parseLinkedList=function(variable){
    var linkedListValue = variable["value"].substr(1, str.length-2).split(',');
    var listLen = variable["length"];
    var head = variable["head"];

    var linkedList = av.ds.list();
    var temp;
    if (linkedListValue.length!=listLen || linkedListValue.length==0 || parseInt(linkedListValue[0])!=head ){
        alert("Invalid input! \n");
        return;
    }
    temp=linkedList.addFirst(head);
    for(var i=1; i<listLen;i++){
        temp=temp.addLast(parseInt(linkedListValue[i]);
        temp.layout();
    }
    return temp;
}

vizJSAV.prototype.parseGraph=function(variable){

    var vertexList = variable["vertexList"];
    var edgeList = variable["edgeList"];

    var noVertexes = variable["no_nodes"];
    var noEdges = variable["no_edges"];

    var graph = av.ds.graph({layout: "automatic"});
    
    var currentV, currentE, startNode, endNode, startNodeIndex, endNodeIndex, edgeWeight;
    var vertexList={};
    
    if (noVertexes != vertexList.length ||noEdges!=edgeList.length ){
        alert('Invalid input!\n');
        return;
    }

    for (var i=0; i<vertexList.length; i++){
        currentV=vertexList[i];
        var currentVP = graph.addNode(currentV["value"]);
        currentVP.css("{color:"+currentV["color"]+";}");
        vertexList[currentV["value"]=currentVP;
        graph.layout();
    }
    for (var i=0; i<edgeList.length; i++){
        currentE = edgeList[i];
        startNode = vertexList[currentE["start"]];
        endNode = vertexList[currentE["end"]];
        var currentEdge = graph.addEdge(startNode, endNode, {weight: currentE["weight"]});
        currentEdge.label(currentE["weight"]);
        graph.layout();
    }
    return graph;

}

vizJSAV.prototype.parseBTree=function(variable){
	var tree = av.ds.tree();
    var optStack = [];
    var nodeStack = [];
    var token = "";
    var parent;
    var node;
    var str = variable["value"];

    for (var i=0; i<str.length;i++){
        switch(str[i]){
            case '[': 
                optStack.push(str[i]);
                break;
            case ']': 
                if (optStack.length==0){
                    tree.root(nodeStack.pop());
                    tree.layout();
                }else{
                    node=nodeStack.pop();
                    if (node.value()<nodeStack[nodeStack.length-1].value()){
                        nodeStack[nodeStack.length-1].left(node);
                    }else{
                        nodeStack[nodeStack.length-1].right(node);
                    }
                }
                break;
            default:
                while(str[i]!='['&& str[i]!=']'){
                   token=token+str[i];
                   i=i+1;
                }
                token = token.trim().replace(/\'/g, "").replace(/\"/g, "");
                if (token!="None"){
                    node = tree.newNode(token);
                    tree.layout();
                    nodeStack.push(node);    
                }
        }
    }
}


/*
function readTextFile(file)
{
    var xmlFile = new XMLHttpRequest();
    xmlFile.open("GET", file, false);
    xmlFile.send(null);
    var responsexml = xmlFile.responseXML;
    return responsexml
}

vizJSAV.prototype.refresh = function()
{

    // read file
    var xmldoc = readTextFile("varList.xml");
    
    var varList = xmldoc.getElementsByTagName("var");

    for (var i = 0; i < varList.length; i ++)
    {
       var nodeTemp = varList[i].childNodes;
       var varAttr=new arrary;
       var varValue;
       for (var j=0; j<nodeTemp.length;j++){
            if (nodeTemp[j].nodeName=="value")
                varValue=nodeTemp[j].nodeValue;
            else if (nodeTemp[j].nodeName=="attr")
                varAttr.push(nodeTemp[j]);
       }
       var varInfo = [varList[i].getAttribute("name"),
                  varList[i].getAttribute("type"),
                  varValue];
        this.plotVar(varInfo, varAttr);
    }

}
*/