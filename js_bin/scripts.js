function createCookie(name,value,days) {
		if (days) {
			var date = new Date();
			date.setTime(date.getTime()+(days*24*60*60*1000));
			var expires = "; expires="+date.toGMTString();
		}
		else var expires = "";
		document.cookie = name+"="+value+expires+"; path=/";
	}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function check_q(qid) {
  var ans = $("input:radio[name="+qid+"]:checked").val()
  createCookie('l'+level+qid,ans,36500)
  if (ans == "a") {
    if ($("#"+qid+"_a_msg").html()!="") { $("#"+qid+"_a_msg").show(); } else { $("#"+qid+"_a_msg").hide(); }
    $("#"+qid+"_b_msg").hide();
    $("#"+qid+"_c_msg").hide();
    $("#"+qid+"_d_msg").hide();
    $("#"+qid+"_e_msg").hide();
  } else if (ans == "b") {
    $("#"+qid+"_a_msg").hide();
    if ($("#"+qid+"_b_msg").html()!="") { $("#"+qid+"_b_msg").show(); } else { $("#"+qid+"_b_msg").hide(); }
    $("#"+qid+"_c_msg").hide();
    $("#"+qid+"_d_msg").hide();
    $("#"+qid+"_e_msg").hide();
  } else if (ans == "c") {
    $("#"+qid+"_a_msg").hide();
    $("#"+qid+"_b_msg").hide();
    if ($("#"+qid+"_c_msg").html()!="") { $("#"+qid+"_c_msg").show(); } else { $("#"+qid+"_c_msg").hide(); }
    $("#"+qid+"_d_msg").hide();
    $("#"+qid+"_e_msg").hide();
  } else if (ans == "d") {
    $("#"+qid+"_a_msg").hide();
    $("#"+qid+"_b_msg").hide();
    $("#"+qid+"_c_msg").hide();
    if ($("#"+qid+"_d_msg").html()!="") { $("#"+qid+"_d_msg").show(); } else { $("#"+qid+"_d_msg").hide(); }
    $("#"+qid+"_e_msg").hide();
  } else if (ans == "e") {
    $("#"+qid+"_a_msg").hide();
    $("#"+qid+"_b_msg").hide();
    $("#"+qid+"_c_msg").hide();
    $("#"+qid+"_d_msg").hide();
    if ($("#"+qid+"_e_msg").html()!="") { $("#"+qid+"_e_msg").show(); } else { $("#"+qid+"_e_msg").hide(); }
  }
  return ans;
}

function find_sec() {
  timer_text = $('#timer').val().split(":");
  if ((timer_text[0]*1 >= 0) & (timer_text[1]*1 >= 0) & (timer_text[2]*1 >= 0)) {
    seconds = timer_text[2]*1, minutes = timer_text[1]*1, hours = timer_text[0]*1;
    t = seconds + minutes*60 + hours*60*60;
    createCookie('l'+level+'timer',$('#timer').val(),36500);
  } else {
    $('#timer').val( (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds) );
    alert('There was a problem with you time entry. It must be of the form 00:00:00. \nIt has been reset to the value it held before your edit.');
  }
}

function add() {
    // inspired by https://jsfiddle.net/Daniel_Hug/pvk6p/

    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }

    $('#timer').val( (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds) );

    timer();
}
function timer() {
    t = setTimeout(add, 1000);
    //if (t % 2 == 0) {
    createCookie('l'+level+'timer',$('#timer').val(),36500);
    //}
}

function start_time() {
  timer();
  $('#play').hide();
  $('#pause').show();
  $('#timer_div').css("background-color", "#c2fcd8");
  $('#timer').css("background-color", "#c2fcd8");
}

function pause_time() {
  clearTimeout(t);
  $('#play').show();
  $('#pause').hide();
  $('#timer_div').css("background-color", "white");
  $('#timer').css("background-color", "white");
}

if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
 $('#timer_div').css("display", "none");
}
