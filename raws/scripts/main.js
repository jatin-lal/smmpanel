(function(){
	if (document.getElementById("request-proposal")) {
		document.getElementById("request-proposal").onclick = function(event) {
		document.getElementsByTagName("BODY")[0].style.overflow = "hidden";
			console.log("Clicked on Request Proposal");
			document.getElementById('request-quotation-modal').style.display = "table";
			setTimeout(function(){
				document.getElementById('request-quotation-modal').classList.add('open');
			}, 10);
		}
	}

	if (document.getElementById("request-quotation-cancel")) {
		document.getElementById("request-quotation-cancel").onclick = function(event) {
			document.getElementsByTagName("BODY")[0].style.overflow = "auto";
			document.getElementById("request-quotation-modal").classList.remove('open');
			setTimeout(function(){
				document.getElementById("request-quotation-modal").style.display = "none";
			}, 500);
		}
	}

	if (document.getElementById('paytm-page')) {
		document.getElementById('amount').oninput = function(){
			document.getElementById('amount_in_usd').innerHTML = "Around <b>" + (this.value / 72).toFixed(2) + " USD</b> will be added to your account ";
			document.getElementById('usd_value').value = (this.value / 70).toFixed(2)
		}
	}

	else if (document.getElementById('bitcoin-page')) {
		function getJSON(url, callback) {
			var xhr = new XMLHttpRequest();
			xhr.open('GET', url, true);
			xhr.responseType = 'json';
			xhr.onload = function() {
				var status = xhr.status;
				if (status === 200) {
					callback(null, xhr.response);
				}
				else {
					callback(status, xhr.response);
				}
			};
			xhr.send();
		};
		getJSON('https://coincap.io/page/BTC/',
			function(err, data) {
				if (err !== null) {
					alert('Something went wrong: ' + err);
				}
				else {
				price = data.price_usd;
				console.log(price);
			}
		});
		document.getElementById('amount').oninput = function(){
			console.log(this.value);
			document.getElementById('amount_in_usd').innerHTML = "Around <b>" + (this.value * price).toFixed(2) + " USD</b> will be added to your account ";
			document.getElementById('usd_value').value = (this.value * price).toFixed(2);
		}
	}

	else if (document.getElementById('ethereum-page')) {
		function getJSON(url, callback) {
			var xhr = new XMLHttpRequest();
			xhr.open('GET', url, true);
			xhr.responseType = 'json';
			xhr.onload = function() {
				var status = xhr.status;
				if (status === 200) {
					callback(null, xhr.response);
				}
				else {
					callback(status, xhr.response);
				}
			};
			xhr.send();
		};

		getJSON('https://coincap.io/page/ETH',
			function(err, data) {
				if (err !== null) {
					alert('Something went wrong: ' + err);
				}
				else {
				price = data.price_usd;
				console.log(price);
			}
		});

		document.getElementById('amount').oninput = function(){
			console.log(this.value);
			document.getElementById('amount_in_usd').innerHTML = "Around <b>" + (this.value * price).toFixed(2) + " USD</b> will be added to your account ";
			document.getElementById('usd_value').value = (this.value * price).toFixed(2)
		}
	}

	if (document.getElementById("start-fetch-usernames")) {
		document.getElementById("start-fetch-usernames").onclick = function(event) {
			event.preventDefault();
			document.getElementById("telegram-members-modal").style.display = "table";
			setTimeout(function() {
				document.getElementById("telegram-members-modal").classList.add("open");
			});
		}
	}

	if (document.getElementById("close-box")) {
		document.getElementById("close-box").onclick = function(event) {
			document.getElementById("telegram-members-modal").classList.remove("open");
			setTimeout(function() {
				document.getElementById("telegram-members-modal").style.display = "none";
			}, 510);
		}
	}

	if (document.getElementById("telegram-start-button")) {
		console.log("/api/get-members?group-name=" + document.getElementById("group-name").value);
		document.getElementById("telegram-start-button").onclick = function(event) {
			document.getElementById('telegram-members-overlay').style.display = "block";
			function getJSON(url, callback) {
				var xhr = new XMLHttpRequest();
				xhr.open('GET', url, true);
				xhr.responseType = 'json';
				xhr.onload = function() {
					var status = xhr.status;
					if (status === 200) {
						callback(null, xhr.response);
					}
					else {
						callback(status, xhr.response);
					}
				};
				xhr.send();
			};
			getJSON('/api/get-members?group-name=' + document.getElementById("group-name").value,
				function(err, data) {
					if (err !== null) {
						alert('Something went wrong: ' + err);
					}
					else {
						document.getElementById('telegram-members-modal').style.display = "none";
						window.location="/dashboard/orders";
					}
				}
			);
		}
	}

	if (document.getElementById('members-sheet')) {
		str = "";
		arr = document.getElementById("members-list").innerHTML.split("@");
		for (i = 0;i < arr.length; i++) {
			if (arr[i] != "") {
				str = str + "<p>@" + arr[i] + "</p>";
			}
		}
		document.getElementById("members-list").innerHTML = str;
	}

	if (document.getElementById('order_quantity')) {
	    loadOptions();
	}

	if (document.getElementById("banner")) {
		window.onscroll = function(event) {
			if (document.documentElement.scrollTop > 10) {
				nav = document.getElementById("nav");
				if (!nav.classList.contains("down")) {
					nav.classList.add("down");
				}
			}
			else{
				if (nav.classList.contains("down")) {
					nav.classList.remove("down");
				}
			}
		}
	}
	
	if (document.getElementById("preloader")) {
		setTimeout(function(){
			document.getElementById("preloader").classList.add("closing");
			setTimeout(function() {
				document.getElementById("preloader").style.display = "none";
			}, 500);
		}, 10);
	}
})();

function loadOptions() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = this.responseText;
            var obj = JSON.parse(data);
            services_select = document.getElementById('services_select');
            options = services_select.innerHTML;
            for (i = 0; i < Object.keys(obj).length; i++) {
                options += '<option data-min="' + obj[i]['min'] + '" data-max="' + obj[i]['max'] + '" data-price="' + obj[i]['rate'] + '" value="' + obj[i]['name'] + '">' + obj[i]['name'] + '</option>';
            }
            services_select.innerHTML = options;
            document.getElementById('place_order_spinner').classList.add('closing');
            setTimeout(function(){
            	document.getElementById('place_order_spinner').style.display = 'none';
            }, 250);
        }
    };
    xhttp.open("GET", "/api/get-services", true);
    xhttp.send();
}

if (document.getElementById('order_quantity')) {
	document.getElementById('order_quantity').oninput = function() {
	    sel = document.getElementById('services_select');
	    var opt = sel.options[sel.selectedIndex].dataset.price;
	    quantity = this.value;
	    quantity = document.getElementById('order_quantity').value;
	    final_amount = parseFloat(opt) * parseInt(quantity) / 1000;
	    if (final_amount > 0) {
	        document.getElementById('final-amount').innerHTML = "<p>Total charge : " + final_amount + "$</p>";
	    } else {
	        document.getElementById('final-amount').innerHTML = "";
	    }
	    document.getElementById('price_deduct').value = final_amount;
	}
}

if (document.getElementById('order_quantity')) {
	document.getElementById('services_select').onchange = function() {
	    console.log("Changed services");
	    sel = document.getElementById('services_select');
	    var opt = sel.options[sel.selectedIndex].dataset.price;
	    if (opt > 0) {
	        document.getElementById('ppk').innerHTML = "<p>Charges per thousand is " + opt + "$</p><p>Minimum quantity is " + sel.options[sel.selectedIndex].dataset.min + "</p><p>Maximum quantity is " + sel.options[sel.selectedIndex].dataset.max + "</p>";
	    } else {
	        document.getElementById('ppk').innerHTML = "";
	    }
	}
}