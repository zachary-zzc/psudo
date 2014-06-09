var av;

function initiateBlock(blockID){
	av = new JSAV(blockID);

}

function vizJSAV(am, w, h){
	this.init(am, w, h);
	av.umsg("Ready!", {"color": "blue"});
    vizJSAV.prototype.refresh(); 
}

function readTextFile(file)
{
    var xmlFile = new XMLHttpRequest();
    xmlFile.open("GET", file, false);
    xmlFile.send(null);
    var responsexml = xmlFile.responseXML;
    return responsexml
}

vizJSAV.prototype.plotVar = function(varInfo, varAttr){

    var varName = varInfo[0].trim();
    var varType = varInfo[1].trim(); 
    var varValueStr = varInfo[2].trim();
    var varValue;
    var avVar;
    switch (varType){
        case "list": 
            varValue = this.parseList(varValueStr);
            avVar= av.ds.array(avValue);
            break;
        case "int": 
            varValue = this.parseInt(varValueStr);
            break;
        case "matrix": 
            varValue = this.parseMatrix(varValueStr, varAttr);
            avVar=av.ds.matrix(varValue);
            break;
        case "heap": 
            varValue = this.parseHeap(varValueStr, varAttr);
            avVar=av.ds.array(varValue);
            break;
        case "BTree": 
            avVar=this.parseBTree(varValueStr, varAttr);
            break;
        case "Graph": 
            avVar = this.parseGraph(varValueStr, varAttr);
            break;
        case "linkedList":
            avVar = this.parseLinkedList(varValueStr, varAttr);

        default: break;
    }
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

vizJSAV.prototype.parseList=function(str){
	var list = new array();
	var len = str.length;
	if (str[0]=='(' && str[len-1]==')'){
		var i =1;
		while (str[i]!=')'){
			list.push(str[i]);
			i=i+1;
		}
		return list;
	}else{
		alert("Invalid input! \n");
	}
}

vizJSAV.prototype.parseHeap=function(str, attrs){
	var isEmpty =  attrs.getNamedItem("isEmpty");
	if (isEmpty || !(str[0]=='(' && str[len-1]==')'))
		alert("Invalid input! \n");
	else
		return this.parseList(str);
}

vizJSAV.prototype.parseMatrix=function(str, attrs){
	var matrixStr=str.substr(1, str.len-2);
	var nCols=attrs.getNamedItem("ncols");
	var nRows=attrs.getNamedItem("nrows");
	var rows = matrixStr.split(']');
	var matrix = new array();
	if (rows.length!= nRows){		
		alert("Invalid input! \n");
		return;
	}else{
		for (var i=0; i<nRows;i++){
			rows[i].replace('[','');
			var tempRow = rows[i].split(',');
			tempRow=tempRow.join('').split('');//remove empty cells
			if (tempRow.length!=nCols){				
				alert("Invalid input! \n");
				return;
			}
			matrix.push(tempRow);
		}
		return matrix;
	}
}

vizJSAV,prototype.parseLinkedList=function(str, attrs){
    var linkedListValue = str.substr(1, str.length-2).split(',');
    var listLen = attrs.getNamedItem("length");
    var linkedList = av.ds.list();
    var temp;
    if (linkedListValue.length!=listLen || linkedListValue.length==0){
        alert("Invalid input! \n");
        return;
    }else{
        temp=linkedList.addFirst(linkedListValue[0]);
        for(var i=1; i<linkedListValue.length;i++){
            temp=temp.addLast(linkedListValue[i]);
        }
    }
    return linkedList;
}

vizJSAV.prototype.parseGraph=function(str, attrs){
    var vertexes = attrs.childNodes.getNamedItem("V");
    var edges = attrs.childNodes.getNamedItem("E");

    var noVertexes = attrs.childNodes.getNamedItem("vertex_count");
    var noEdges = attrs.childNodes.getNamedItem("edge_count");
    var graph = av.ds.graph({layout: "automatic"});
    
    var currentV, adjVList, startNode, endNode, startNodeIndex, endNodeIndex, edgeWeight;
    var vertexList={};
    
    if (noVertexes != vertexes.length ||noEdges!=edges.length ){
        alert('Invalid input!\n');
        return;
    }else{
        for (var i=0; i<vertexes.length; i++){
            currentV=vertexes[i].attributes.getNamedItem("value");
            var currentVP = graph.addNode(currentV);
            vertexList[currentV]=currentVP;
        }
        for (var i=0; i<edges.length; i++){
            startNodeIndex = edges.attributes.getNamedItem("start_point");
            endNodeIndex = edges. attributes.getNamedItem("end_point");
            edgeWeight = edges. attributes.getNamedItem("weight");

            startNode = vertexList[startNodeIndex];
            endNode = vertexList[endNodeIndex];
            graph.addEdge(startNode, endNode, {weight: edgeWeight});
        }
        return graph;
    }
}

vizJSAV.prototype.parseBTree=function(str){
	var tree = av.ds.tree();
    var optStack = [];
    var nodeStack = [];
    var token = "";
    var parent;
    var node;
    for (var i=0; i<str.length;i++){
        switch(str[i]){
            case '[': 
                optStack.push(str[i]);
                break;
            case ']': 
                if (optStack.length==0){
                    tree.root(nodeStack.pop());
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
                    nodeStack.push();    
                }
        }
    }
}


