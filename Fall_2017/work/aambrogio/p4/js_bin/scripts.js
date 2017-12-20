function fedpov(house,income,percentage){
// Determines if your income is less than or equal to 
// a percentage of the federal poverty guidlines for 
// the contiguous United States.
	
	var line = NaN;
	
	if (house == 1) {
		line = 12060;
	} else if (house == 2) {
		line = 16240;
	} else if (house == 3) {
		line = 20420;
	} else if (house == 4) {
		line = 24600;
	} else if (house == 5) {
		line = 28780;
	} else if (house == 6) {
		line = 32960;
	} else if (house == 7) {
		line = 37140;
	} else if (house == 8) {
		line = 41320;
	} else if (house > 8) {
		line = 41320 + (house-8)*4180;
	}
	
	if (income <= (line*(percentage/100))) {
		return true;
	} else {
		return false;
	}
}


function sixmedinc(house,income){
// Determines if your income is less than or equal to 
// 60% of the median income for Mass. 
	
	var line = NaN;
	
	if (house == 1) {
		line = 34380;
	} else if (house == 2) {
		line = 44958;
	} else if (house == 3) {
		line = 55537;
	} else if (house == 4) {
		line = 66115;
	} else if (house == 5) {
		line = 76693;
	} else if (house == 6) {
		line = 87272;
	} else if (house == 7) {
		line = 89255;
	} else if (house == 8) {
		line = 91239;
	} else if (house == 9) {
		line = 93222;
	} else if (house == 10) {
		line = 95206;
	} else if (house == 11) {
		line = 97189;
	} else if (house == 12) {
		line = 99173;
	} else if (house == 13) {
		line = 101156;
	} else if (house == 14) {
		line = 103139;
	} else if (house == 15) {
		line = 105123;
	} else if (house == 16) {
		line = 107106;
	} else if (house == 17) {
		line = 109090;
	} else {
		alert("Note: Cannot accept household of more that 17.");
	}
	
	if (income <= line) {
		return true;
	} else {
		return false;
	}
}
