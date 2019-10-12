function resetid(){
	for(var i=1;i<17;i++)
	{
		var page ="page"+i;
		document.getElementById(page).className ="trash"
	}
}

async function forfunction(page){
	document.getElementById("contentdiv").innerHTML ="<div id  =\"temp\"><h1 style=\"color:Orange\">Fetching Images. Please be Patient </h1> <br>"+
	" <h3 style=\"color:Orange\">Switch to python console to see progress</h3></div>";
	let value= await eel.getPageData(page.toString(),"1")();
	var length = value.length;
	var i;
	for (i=0;i<length;i++){
	showImage(value[i][0],value[i][1]);}
	resetid();
	document.getElementById("temp").innerHTML="";
	document.getElementById("page"+page).className ='active';
}

function showImage(magId,issueId) {
	var src = "../mag_images/"+magId+"/"+issueId+".jpg";
	var img = document.createElement("img");
	img.src = src;
	img.width = 212;
	img.height = 300;
	// generate page
	img.onclick =async function(){
		var img_magid = magId;
		var img_issueId =issueId;
		document.getElementById("contentdiv").innerHTML ="<div id=\"temp\"><h1 style=\"color:Orange\">Fetching Images. Please be Patient </h1> <br>"+
		" <h3 style=\"color:Orange\">Switch to python console to see progress</h3></div>";
		// add getElementById
		// update button
		var buttondiv = document.createElement("div");
		buttondiv.setAttribute("id","buttondiv");
		var updatebutton  = document.createElement("button");
		updatebutton.type ="button";
		updatebutton.className = "btn btn-info";
		updatebutton.id = "updateIssue";
		updatebutton.style ="margin-left: 42%; margin-top: 1%; background-color : #EC971F; border-color : #E7892B;";
		updatebutton.innerHTML="Update Issue Database";
		updatebutton.onclick =async function(){
		let tempvar = await eel.updateIssueDataBase(magId);
		};
		document.getElementById("contentdiv").appendChild(buttondiv);
		document.getElementById("buttondiv").appendChild(updatebutton);
			let imagearr  = await eel.getImagebyID(img_magid,img_issueId)();
			var length = imagearr.length;
			var i;
			for (i=0;i<length;i++){
			showImage2(imagearr[i][0],imagearr[i][1]);}
			document.getElementById("temp").innerHTML = "";
	};
	document.getElementById("contentdiv").appendChild(img);}

function showImage2(magId,issueId){
	var src = "../mag_images/"+magId+"/"+issueId+".jpg";
	var img = document.createElement("img");
	img.src = src;
	img.width = 212;
	img.height = 300;
	// generate page
	img.onclick =async function(){
		var img_magid = magId;
		var img_issueId =issueId;
		document.getElementById("contentdiv").innerHTML ="<h1 style=\"color:Orange\">Downloding file magID -"+img_magid+" issueId -"+img_issueId+". Please be Patient</h1> <br> "+
		"<h3 style=\"color:Orange\">Switch to python console to see progress</h3><br>"+
		"<h3 style=\"color:Orange\">Delete the above file if download fails.</h3>";
		let re = await eel.downloadPDF(img_magid,img_issueId)();
		document.getElementById("contentdiv").innerHTML = "<h2 style=\"color:Orange\">"+img_magid+"  "+img_issueId+"</h2><br>"+
		"<h3 style=\"color:Orange\">Delete the file if PDF is not opening.</h3>";
		var ifrm =document.createElement("iframe");
		ifrm.setAttribute("src","../downloads/"+img_magid+"/"+img_issueId+".pdf#page=1&zoom=150");
		ifrm.setAttribute("width","100%");
		ifrm.setAttribute("style","height:66em");
		document.getElementById("contentdiv").appendChild(ifrm);
	};
	document.getElementById("contentdiv").appendChild(img);}
