var av;
var jsonPath= 'json_temp.js';
var jsonContent;

$(document).ready(

    function(){
        $.getJSON(jsonPath, function(data){
            jsonContent = data;
        }
        );
    } 
 );

function vizJSAV(divID, statIndex){
    var variable;
    var statementLabel ="statement_"+statIndex;
    //alert(statementLabel);
    var variableList = jsonContent[statementLabel]["Vars"];

    av = new JSAV(document.getElementById(divID));

    for (var i =0; i<variableList.length; i++){
        variable = variableList[i]; 
        //alert(variable.type);
        if (variable != null){
            this.plotVar(variable);
        }
    }
}


vizJSAV.prototype.setCSSByClass=function(objclass,cssStr){
    var objs = document.getElementsByClassName(objclass);
    for (var i=0; i<objs.length;i++){
        objs[i].css(cssStr);    
    }
}

//indices is a list of elements to be highligted[1.2,3]
vizJSAV.prototype.arrayHighlight=function(array, indices){
    array.highlight(indices);
}
vizJSAV.prototype.arrayUnhighlight=function(array, indices){
    array.unhighlight(indices);
}
vizJSAV.prototype.linkedListHighlight=function(linkedList, index){
    linkedList.get(index).highlight();
}
vizJSAV.prototype.linkedListUnhighlight=function(linkedList, index){
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
            avVar =av.ds.array([varValue])
            break;
        case "list": 
            varValue = this.parseList(variable);
            avVar= av.ds.array(varValue);
            avVar.addClass("list");
            break;
        case "stack": 
            varValue = this.parseList(variable);
            avVar=av.ds.array(varValue, {layout:"vertical"});
            avVar.addClass("stack");
            break;
        case "matrix": 
            varValue = this.parseMatrix(variable);
            avVar=av.ds.matrix(varValue);
            avVar.addClass("matrix");
            break;
        case "BTree": 
            avVar=this.parseBTree(variable);
            avVar.addClass("BTree");
            break;
        case "Graph": 
            avVar = this.parseGraph(variable);
            avVar.addClass("Graph");
            break;
        case "LinkedList":
            avVar = this.parseLinkedList(variable);
            avVar.addClass("LinkedList");
        default: break;
    }
}



vizJSAV.prototype.parseList=function(variable){
	var list = [];
	var len = variable["length"];
    var valueStr = variable["value"];
    
    //alert(valueStr[0]+valueStr[valueStr.length-1]);   
    
    var valueCharList = valueStr.substr(1,valueStr.length-1).split(',');
    
    removeEmptyElementFromArray(valueCharList);

    if (valueStr[0]!='(' || valueStr[valueStr.length-1]!=')' || valueCharList.length != len){
        //alert("Invalid array! \n");
        return [];
    }
    //alert("length:"+valueCharList.length);
    for (var i=0; i<len; i++){
        list.push(parseInt(valueCharList[i]));
    }
    return list;
}

/*
vizJSAV.prototype.parseStack=function(variable){
	var isEmpty =  variable["isEmpty"];
    alert(variable["value"]);
	if (isEmpty){
		//alert("Invalid input! \n");
        return [];
    }
	return this.parseList(variable);
}
*/
function removeEmptyElementFromArray(array){
    for (var i =array.length-1; i>=0; i--){
                    if (array[i]=='')
                        array.splice(i,1);
                }
}
vizJSAV.prototype.parseMatrix=function(variable){
	var matrixStr=variable["value"];
    var matrixVal=matrixStr.substr(2, matrixStr.length-4);
	var nCols=variable["n_cols"];
	var nRows=variable["n_rows"];
    //alert(matrixVal);
	var rows = matrixVal.split(']');
    //alert(rows.length+" rows!");
	var matrix = new Array();
	if (rows.length!= nRows){		
		//alert("Invalid matrix! \n");
		return;
	}else{
		for (var i=0; i<nRows;i++){
            rows[i]=rows[i].replace('[','');
            //alert(rows[i]);
			var rowsCharList = rows[i].split(',');
            
            removeEmptyElementFromArray(rowsCharList);

            //alert(rowsCharList.length);

			if (rowsCharList.length!=nCols){				
				//alert("Invalid input! \n");
				return;
			}

            var tempRow = new Array();
            for (var j=0; j<rowsCharList.length;j++){
                tempRow.push(parseInt(rowsCharList[j]));
            } 
                
			matrix.push(tempRow);
		}
		return matrix;
	}
}

vizJSAV.prototype.parseLinkedList=function(variable){
    var linkedListStr = variable["value"];
    var linkedListValue = (linkedListStr.substr(1, linkedListStr.length-2)).split(',');
    var listLen = variable["length"];
    var head = variable["head"];

    var linkedList = av.ds.list();
    var tempList, tempNode;
    if (linkedListValue.length!=listLen || linkedListValue.length==0 || parseInt(linkedListValue[0])!=head ){
        //alert("Invalid input! \n");
        return;
    }
    tempList=linkedList.addFirst(head);
    for(var i=1; i<listLen; i++){
        tempNode = parseInt(linkedListValue[i]);
        tempList=tempList.addLast(tempNode);
        tempList.layout();
    }
    linkedList = tempList;
    return linkedList;
}

vizJSAV.prototype.parseGraph=function(variable){
    //alert("Here is a graph!");
    var vertexList = variable["vertexList"];
    var edgeList = variable["edgeList"];
    var noVertexes = variable["no_nodes"];
    var noEdges = variable["no_edges"];
    var graph = av.ds.graph({width: 800, height: 400, layout: "automatic"});
    var vertexDict= {};
    var currentV, currentE, currentEdge, startNode, endNode, edgeWeight;
    
    if (noVertexes != vertexList.length ||noEdges!=edgeList.length ){
        //alert('Invalid graph!\n');
        return;
    }

    for (var i=0; i<vertexList.length; i++){
        currentV=vertexList[i];
        var currentVP = graph.addNode(currentV["value"]);
        currentVP.css("{color:"+currentV["color"]+";}");
        vertexDict[currentV["value"]]=currentVP;
        graph.layout();
    }
    for (var i=0; i<edgeList.length; i++){
        currentE = edgeList[i];
        startNode = vertexDict[currentE["start"]];
        endNode = vertexDict[currentE["end"]];
        currentEdge = graph.addEdge(startNode, endNode, {weight: currentE["weight"]});
        currentEdge.label(currentE["weight"]);
        graph.layout();
    }

    graph.layout();
    return graph;
}

vizJSAV.prototype.parseBTree=function(variable){
	var tree = av.ds.binarytree();
    var optStack = [];
    var nodeStack = [];
    var token = "";
    var parent;
    var node;
    var str = variable["value"];
    var tempLast;
    for (var i=0; i<str.length;i++){
        switch(str[i]){
            case '[': 
                optStack.push(str[i]);
                //alert("new node start!");
                break;
            case ']': 
                //alert("a node closed!");
                optStack.pop();
                if (optStack.length==0){
                    node=nodeStack.pop();
                    tree.root(node);
                    //alert(node.value());
                    tree.layout();
                }else{
                    node=nodeStack.pop();
                    //alert(node.value());
                    tempLast=optStack.length-1;
                    if (node.value()<nodeStack[tempLast].value()){
                        nodeStack[tempLast].left(node);
                        tree.layout();
                    }else{
                        nodeStack[tempLast].right(node);
                        tree.layout();
                    }   
                }
                break;
            default:
                token=token+str[i];
                if (str[i+1]=='[' || str[i+1]==']'){
                    token = token.trim().replace(/\'/g, "").replace(/\"/g, "");
                    if (token!="None"){
                    node = tree.newNode(token);
                    nodeStack.push(node); 
                    //alert(node.value()+" is created!");   
                    }   
                    token="";//reset token
                }
                
            /*
                while(!(str[i]=='[' || str[i]==']')){
                   token=token+str[i];
                   i=i+1;
                }
                token = token.trim().replace(/\'/g, "").replace(/\"/g, "");
                if (token!="None"){
                    node = tree.newNode(token);
                    nodeStack.push(node); 
                    //alert(node.value()+" is created!");   
                }
                token="";//reset token
                i=i-1;//reset i
*/        }
    }
    tree.layout();
    return tree;
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