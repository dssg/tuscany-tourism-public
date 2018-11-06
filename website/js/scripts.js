$(document).ready(function () {
	"use strict";

	const iframePath = "./graphics/";
	function getDesc(description) {
		return (
			"<div><h6>Description</h6><div style='background-color:#FEFEFE; margin-top: 15px; margin:30px; border-width: 1px; border-style: solid; border-radius: 5px; padding: 10px; border-color: #F0F0F0;'>" + description + "</div ></div> "
		)
	}
	function getHTML(name) {
		let val =
			`<iframe src='${iframePath}${name}' style = 'border:none; height:100%;width:100%;' ></iframe >`

		return (
			`<div class='col-lg-12 col-md-12 col-sm-12 plot-iframe'>${val}</div>`
		)

	}

	function getSelections(values) {
		if (values) {
			return values.map((value) => {
				return `<option value='${value}' >${value}</option>`
			})
		}
	}

	function getArrHTML(arr) {
		console.log("arr", arr)
		if (arr) {
			let val = arr.map((name) => {
				return (
					`<div class='col-lg-12 col-md-12 col-sm-12' style='height:800px' > <iframe src='${iframePath}${name}' style='border:none; height:100%;width:100%;' ></iframe></div >`
				)
			})
			return (
				val
			)
		}
	}

	$('#plotly-locations').html(getHTML(dictionaryObj.locations[0].value))
	$('#plotly-personas').html(getHTML(dictionaryObj.personas[0].value))
	$('#plotly-trajectories').html(getHTML(dictionaryObj.trajectories[0].value))
	$('#locations-description').html(getDesc(dictionaryObj.locations[0].description))
	$('#personas-description').html(getDesc(dictionaryObj.trajectories[0].description))
	$('#trajectories-description').html(getDesc(dictionaryObj.trajectories[0].description))
	$('#trajectory_country').append(getSelections(dropdowns.trajectories[$('#trajectory_season').val()]))
	$('#persona_country').append(getSelections(dropdowns.personas[$('#persona_season').val()]))


	$('#locationGraphChange').click(function () {
		let graphs = dictionaryObj.locations.filter((l) => {
			return l.season == $('#locationBySeason').val()
		})

		let path = graphs[0] ? graphs[0].value : dictionaryObj.locations[0].value
		let description = graphs[0] ? graphs[0].description : dictionaryObj.locations[0].description

		$('#plotly-locations').html(getHTML(path))
		$('#locations-description').html(getDesc(description))
	})



	$('#location_summary_picker').change(() => {
		if ($('#location_summary_picker').val() == "Summary") {
			$('#location_picker_form').hide();
		}
		else {
			$('#location_picker_form').show();
		}
	})



	$('#personaGraphChange').click(function () {
		let graphs = dictionaryObj.personas.filter((p) => {
			console.log(p.season, $('#persona_season').val(), p.country, $('#persona_country').val())
			return p.season == $('#persona_season').val() && p.country == $('#persona_country').val()
		})
		let name = graphs[0] ? graphs[0].value : dictionaryObj.personas[0].value
		let description = graphs[0] ? graphs[0].description : dictionaryObj.personas[0].description
		$('#plotly-personas').html(getHTML(name))
		$('#personas-description').html(getDesc(description))
	})


	$('#persona_summary_picker').change(() => {
		if ($('#persona_summary_picker').val() == "Summary") {
			$('#persona_picker_form').hide();
		}
		else {
			$('#persona_picker_form').show();
		}
	})

	$('#persona_season').change(() => {
		$('#persona_country').find('option').remove()
		$('#persona_country').append(getSelections(dropdowns.personas[$('#persona_season').val()]))
	})

	// Alonso and Orsi awesome code  <3
	$( '#trajectory_summary' ).click(function() {
	  var season = $('#trajectory_season').val();
	  var country = $('#trajectory_country').val();
	  var summary = $(this).val();
	  var clusters = dropdownsClusters[season][country]

	  var options = clusters.map(function(cluster) {
	  	return '<option>' + cluster + '</option>'; 
	  });

	  $('#trajectory_cluster').html(options);
	});

      

	$('#trajectoryGraphChange').click(function () {

		let graphs = dictionaryObj.trajectories.filter((t) => {
			return (t.season == $('#trajectory_season').val() && t.country == $('#trajectory_country').val() &&
				($('#trajectory_summary').val() == t.cluster || $('#trajectory_cluster').val() == t.cluster))
		})

		let name = graphs[0] ? graphs[0].value : null
		let description = graphs[0] ? graphs[0].description : dictionaryObj.personas[0].description

		if (Array.isArray(name)) {
			$('#plotly-trajectories').html(getArrHTML(name))
		}
		else {
			$('#plotly-trajectories').html(getHTML(name))
		}
		$('#trajectories-description').html(getDesc(description))
	})

	$('#trajectory_season').change(() => {
		$('#trajectory_country').find('option').remove()
		$('#trajectory_country').append(getSelections(dropdowns.trajectories[$('#trajectory_season').val()]))
	})

	$('#trajectory_summary').change(() => {
		if ($('#trajectory_summary').val() == "Summary") {
			$('#trajectory_picker_form').hide();
		}
		else {
			$('#trajectory_picker_form').show();
		}
	})

	// Nav Sticky

	$(window).scroll(function () {
		if ($(window).scrollTop() > 500 && !$('.mobile-toggle').is(":visible")) {
			$('.top-bar').addClass('nav-sticky');
		} else {
			$('.top-bar').removeClass('nav-sticky');
		}
	});

	// Offscreen Nav

	$('.offscreen-toggle').click(function () {
		$('.main-container').toggleClass('reveal-nav');
		$('.offscreen-container').toggleClass('reveal-nav');
		$('.offscreen-menu .container').toggleClass('reveal-nav');
	});

	$('.main-container').click(function () {
		if ($(this).hasClass('reveal-nav')) {
			$('.main-container').toggleClass('reveal-nav');
			$('.offscreen-container').toggleClass('reveal-nav');
			$('.offscreen-menu .container').toggleClass('reveal-nav');
		}
	});

	// Detect logo dimensions and add correct class


	var theImage = new Image();

	var logoWidth = theImage.width;
	var logoHeight = theImage.height;
	var logoRatio = logoWidth / logoHeight;

	if (logoRatio > 2.8) {
		$('.top-bar .logo').addClass('logo-wide');
	}

	if (logoRatio < 2) {
		$('.top-bar .logo').addClass('logo-square');
	}

	// Smooth scroll

	$('.inner-link').smoothScroll({ offset: -96, speed: 800 });

	// Mobile Toggle

	$('.mobile-toggle').click(function () {
		$('nav').toggleClass('open-nav');
	});

	// Fullscreen nav toggle

	$('.fullscreen-nav-toggle').click(function () {
		if (!$('.fullscreen-nav-container').hasClass('show-fullscreen-nav')) {
			$('.fullscreen-nav-container').addClass('show-fullscreen-nav');
			setTimeout(function () {
				$('.fullscreen-nav-container').addClass('fade-fullscreen-nav');
			}, 100);
			$(this).addClass('toggle-icon');
		} else {
			$(this).removeClass('toggle-icon');
			$('.fullscreen-nav-container').removeClass('fade-fullscreen-nav');
			setTimeout(function () {

				$('.fullscreen-nav-container').removeClass('show-fullscreen-nav');
			}, 500);
		}
	});

	$('.fullscreen-nav-container .menu li a').click(function () {
		$('.fullscreen-nav-toggle').removeClass('toggle-icon');
		$('.fullscreen-nav-container').removeClass('fade-fullscreen-nav');
		setTimeout(function () {
			$('.fullscreen-nav-container').removeClass('show-fullscreen-nav');
		}, 500);
	});

	// Margin first section for top bar

	if (!$('nav').hasClass('overlay-bar') && !$('nav').hasClass('contained-bar')) {
		$('.main-container').first().css('margin-top', $('nav').outerHeight());
	}

	$(window).resize(function () {
		if (!$('nav').hasClass('overlay-bar') && !$('nav').hasClass('contained-bar')) {
			$('.main-container').first().css('margin-top', $('nav').outerHeight());
		}
	});

	// Pad first section for overlay bar

	if ($('nav').hasClass('overlay-bar') || $('nav').hasClass('contained-bar')) {
		var currentPad = parseInt($('.main-container').find(':first-child').css('padding-top'));
		var newPad = currentPad + $('nav').outerHeight() - 48;
		if (currentPad > 0) {
			$('.main-container').children(':first').css('padding-top', newPad);
		} else if ($('.main-container').find(':first').hasClass('hero-slider')) {
			var height = parseInt($('.hero-slider .slides li:first-child').outerHeight());
			var newHeight = height + $('nav').outerHeight();
			$('.hero-slider .slides li').css('height', newHeight);
		}
	}


	// Fullwidth Subnavs

	// Position Fullwidth Subnavs fullwidth correctly

	$('.subnav-fullwidth').each(function () {
		$(this).css('width', $('.container').width());
		var offset = $(this).closest('.has-dropdown').offset();
		offset = offset.left;
		var containerOffset = $(window).width() - $('.container').outerWidth();
		containerOffset = containerOffset / 2;
		offset = offset - containerOffset - 15;
		$(this).css('left', -offset);
	});

	$(window).resize(function () {
		$('.subnav-fullwidth').each(function () {
			$(this).css('width', $('.container').width());
			var offset = $(this).closest('.has-dropdown').offset();
			offset = offset.left;
			var containerOffset = $(window).width() - $('.container').outerWidth();
			containerOffset = containerOffset / 2;
			offset = offset - containerOffset - 15;
			$(this).css('left', -offset);
		});
	});


	// Scroll Reveal

	if (!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
		window.scrollReveal = new scrollReveal();
	} else {
		$('body').addClass('pointer');
	}

	// Slider Initializations

	$('.hero-slider').flexslider({});
	$('.image-slider').flexslider({ animation: "slide" });
	$('.testimonials-slider').flexslider({ directionNav: false });

	// Slide Sizes

	$('.slider-fullscreen .slides li').each(function () {
		$(this).css('height', $(window).height());
	});

	$('.fullscreen-element').each(function () {
		$(this).css('height', $(window).height());
	});


	// Feature Selector

	$('.selector-tabs li').click(function () {
		$(this).parent('.selector-tabs').children('li').removeClass('active');
		$(this).addClass('active');

		var activeTab = $(this).index() + 1;

		$(this).closest('.feature-selector').find('.selector-content').children('li').removeClass('active');
		$(this).closest('.feature-selector').find('.selector-content').children('li:nth-child(' + activeTab + ')').addClass('active');
	});

	// Append .background-image-holder <img>'s as CSS backgrounds

	$('.background-image-holder').each(function () {
		var imgSrc = $(this).children('img').attr('src');
		$(this).css('background', 'url("' + imgSrc + '")');
		$(this).children('img').hide();
		$(this).css('background-position', '50% 0%');
	});

	// Accordion

	$('.accordion li').click(function () {
		$(this).parent('.accordion').children('li').removeClass('active');
		$(this).addClass('active');
	});

	/************** Parallax Scripts **************/

	var isFirefox = typeof InstallTrigger !== 'undefined';
	var isIE = /*@cc_on!@*/ false || !!document.documentMode;
	var isChrome = !!window.chrome;
	var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
	var prefix;

	if (isFirefox) {
		prefix = '-moz-';
	} else if (isIE) {

	} else if (isChrome || isSafari) {
		prefix = '-webkit-';
	}

	$('.main-container section:first-child').addClass('first-child');

	$('.parallax-background').each(function () {

		if ($(this).closest('section').hasClass('first-child') && !$(this).closest('section').hasClass('slider-fullscreen')) {
			$(this).attr('data-top', prefix + 'transform: translate3d(0px,0px, 0px)');
			$(this).attr('data-top-bottom', prefix + 'transform: translate3d(0px,200px, 0px)');

		} else {

			$(this).attr('data-bottom-top', prefix + 'transform: translate3d(0px,-100px, 0px)');
			$(this).attr('data-center', prefix + 'transform: translate3d(0px,0px, 0px)');
			$(this).attr('data-top-bottom', prefix + 'transform: translate3d(0px,100px, 0px)');

		}

	});

	if (!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
		skrollr.init({
			forceHeight: false
		});

		// Multi Layer Parallax

		$('.hover-background').each(function () {
			$(this).mousemove(function (event) {
				$(this).find('.background-image-holder').css('transform', 'translate(' + -event.pageX / 30 + 'px,' + -event.pageY / 45 + 'px)');
				$(this).find('.layer-1').css('transform', 'translate(' + -event.pageX / 50 + 'px,' + -event.pageY / 50 + 'px)');
				$(this).find('.layer-2').css('transform', 'translate(' + -event.pageX / 60 + 'px,' + -event.pageY / 60 + 'px)');
			});
		});
	}

	// Map Holder Overlay

	$('.map-holder').click(function () {
		$(this).addClass('on');
	});

	$(window).scroll(function () {
		if ($('.map-holder').hasClass('on')) {
			$('.map-holder').removeClass('on');
		}
	});

	// Map Details Holder

	$('.details-holder').each(function () {
		$(this).css('height', $(this).width());
	});

	$('.details-holder').mouseenter(function () {
		$(this).closest('.map-overlay').addClass('fade-overlay');
	}).mouseleave(function () { $(this).closest('.map-overlay').removeClass('fade-overlay'); });

	// Countdown

	$('.countdown').each(function () {
		$(this).countdown({ until: new Date($(this).attr('data-date')) });
	});

	// Twitter Feed
	jQuery('#tweets').each(function (index) {
	}).each(function (index) {

		var TweetConfig = {
			"id": jQuery('#tweets').attr('data-widget-id'),
			"domId": '',
			"maxTweets": 5,
			"enableLinks": true,
			"showUser": false,
			"showTime": false,
			"dateFunction": '',
			"showRetweet": false,
			"customCallback": handleTweets
		};
		function handleTweets(tweets) {
			var x = tweets.length;
			var n = 0;
			var element = document.getElementById('tweets');
			var html = '<ul class="slides">';
			while (n < x) {
				html += '<li>' + tweets[n] + '</li>';
				n++;
			}
			html += '</ul>';
			element.innerHTML = html;
			return html;
		}
		twitterFetcher.fetch(TweetConfig);
	});

	// Contact form code

	$('form.email-form').submit(function (e) {
		// return false so form submits through jQuery rather than reloading page.
		if (e.preventDefault) e.preventDefault();
		else e.returnValue = false;

		var thisForm = $(this).closest('.email-form'),
			error = 0,
			originalError = thisForm.attr('original-error'),
			loadingSpinner;

		if (typeof originalError !== typeof undefined && originalError !== false) {
			thisForm.find('.form-error').text(originalError);
		}


		$(thisForm).find('.validate-required').each(function () {
			if ($(this).val() === '') {
				$(this).addClass('field-error');
				error = 1;
			} else {
				$(this).removeClass('field-error');
			}
		});

		$(thisForm).find('.validate-email').each(function () {
			if (!(/(.+)@(.+){2,}\.(.+){2,}/.test($(this).val()))) {
				$(this).addClass('field-error');
				error = 1;
			} else {
				$(this).removeClass('field-error');
			}
		});


		if (error === 1) {
			$(this).closest('.email-form').find('.form-error').fadeIn(200);
		} else {
			// Hide the error if one was shown
			$(this).closest('.email-form').find('.form-error').fadeOut(200);
			// Create a new loading spinner while hiding the submit button.
			loadingSpinner = $('<div />').addClass('form-loading').insertAfter($(thisForm).find('input[type="submit"]'));
			$(thisForm).find('input[type="submit"]').hide();

			jQuery.ajax({
				type: "POST",
				url: "mail/mail.php",
				data: thisForm.serialize(),
				success: function (response) {
					// Swiftmailer always sends back a number representing numner of emails sent.
					// If this is numeric (not Swift Mailer error text) AND greater than 0 then show success message.
					$(thisForm).find('.form-loading').remove();
					$(thisForm).find('input[type="submit"]').show();
					if ($.isNumeric(response)) {
						if (parseInt(response) > 0) {
							thisForm.find('.form-success').fadeIn(1000);
							thisForm.find('.form-error').fadeOut(1000);
							setTimeout(function () { thisForm.find('.form-success').fadeOut(500); }, 5000);
						}
					}
					// If error text was returned, put the text in the .form-error div and show it.
					else {
						// Keep the current error text in a data attribute on the form
						thisForm.find('.form-error').attr('original-error', thisForm.find('.form-error').text());
						// Show the error with the returned error text.
						thisForm.find('.form-error').text(response).fadeIn(1000);
						thisForm.find('.form-success').fadeOut(1000);
					}
				},
				error: function (errorObject, errorText, errorHTTP) {
					// Keep the current error text in a data attribute on the form
					thisForm.find('.form-error').attr('original-error', thisForm.find('.form-error').text());
					// Show the error with the returned error text.
					thisForm.find('.form-error').text(errorHTTP).fadeIn(1000);
					thisForm.find('.form-success').fadeOut(1000);
					$(thisForm).find('.form-loading').remove();
					$(thisForm).find('input[type="submit"]').show();
				}
			});
		}
		return false;
	});


	// Expanding Lists (updated in Pivot 1.4.0)

	$('.expanding-ul li').click(function () {
		$('.expanding-ul li').removeClass('active');
		$(this).addClass('active');
	});

});

$(window).load(function () {

	"use strict";


	// Align Elements Vertically

	alignVertical();
	alignBottom();

	$(window).resize(function () {
		alignVertical();
		alignBottom();
	});

	// Isotope Projects

	$('.projects-container').isotope({
		itemSelector: '.project',
		layoutMode: 'fitRows'
	});

	$('.filters li').click(function () {
		var current = $(this);

		current.siblings('li').removeClass('active');
		current.addClass('active');

		var filterValue = current.attr('data-filter');
		var container = current.closest('.projects-wrapper').find('.projects-container');
		container.isotope({ filter: filterValue });
	});

	// Isotope contained feature boxes

	$('.contained-features-wrapper').isotope({
		itemSelector: '.no-pad',
		layoutMode: 'masonry',
		masonry: {
			gutter: 0
		}
	});

	// Instagram Feed

	if ($('.instafeed').length) {
		jQuery.fn.spectragram.accessData = {
			accessToken: '1406933036.fedaafa.feec3d50f5194ce5b705a1f11a107e0b',
			clientID: 'fedaafacf224447e8aef74872d3820a1'
		};

		$('.instafeed').each(function () {
			$(this).children('ul').spectragram('getUserFeed', {
				query: $(this).attr('data-user-name')
			});

		});

	}

	if ($('#tweets').length) {
		$('#tweets').flexslider({ directionNav: false, controlNav: false });
	}

	// Remove Loader

	$('.loader').css('opacity', 0);
	setTimeout(function () { $('.loader').hide(); }, 600);

	// Mailchimp/Campaign Monitor Mail List Form Scripts
	$('form.mail-list-signup').on('submit', function () {

		var iFrame = $(this).closest('section, header').find('iframe.mail-list-form'),
			thisForm = $(this).closest('.mail-list-signup'),
			userEmail = $(this).find('.signup-email-field').val(),
			userFullName = $(this).find('.signup-name-field').val(),
			userFirstName = $(this).find('.signup-first-name-field').val(),
			userLastName = $(this).find('.signup-last-name-field').val(),
			error = 0;

		$(thisForm).find('.validate-required').each(function () {
			if ($(this).val() === '') {
				$(this).addClass('field-error');
				error = 1;
			}
			else {
				$(this).removeClass('field-error');
			}
		});

		$(thisForm).find('.validate-email').each(function () {
			if (!(/(.+)@(.+){2,}\.(.+){2,}/.test($(this).val()))) {
				$(this).addClass('field-error');
				error = 1;
			}
			else {
				$(this).removeClass('field-error');
			}
		});

		if (error === 0) {
			iFrame.contents().find('#mce-EMAIL, #fieldEmail').val(userEmail);
			iFrame.contents().find('#mce-LNAME, #fieldLastName').val(userLastName);
			iFrame.contents().find('#mce-FNAME, #fieldFirstName').val(userFirstName);
			iFrame.contents().find('#mce-FNAME, #fieldName').val(userFullName);
			iFrame.contents().find('form').attr('target', '_blank').submit();
		}
		return false;
	});

	// Blog Masonry

	$('.blog-masonry-container').isotope({
		itemSelector: '.blog-masonry-item',
		layoutMode: 'masonry'
	});

	$('.blog-filters li').click(function () {
		var current = $(this);

		current.siblings('li').removeClass('active');
		current.addClass('active');

		var filterValue = current.attr('data-filter');
		var container = current.closest('.blog-masonry').find('.blog-masonry-container');
		container.isotope({ filter: filterValue });
	});



});

function handleTweets(tweets) {
	var x = tweets.length;
	var n = 0;
	var element = document.getElementById('tweets');
	var html = '<ul class="slides">';
	while (n < x) {
		html += '<li>' + tweets[n] + '</li>';
		n++;
	}
	html += '</ul>';
	element.innerHTML = html;
}

function alignVertical() {

	$('.align-vertical').each(function () {
		var that = $(this);
		var height = that.height();
		var parentHeight = that.parent().height();
		var padAmount = (parentHeight / 2) - (height / 2);
		that.css('padding-top', padAmount);
	});

}

function alignBottom() {
	$('.align-bottom').each(function () {
		var that = $(this);
		var height = that.height();
		var parentHeight = that.parent().height();
		var padAmount = (parentHeight) - (height) - 32;
		that.css('padding-top', padAmount);
	});
}


// Youtube Background Handling

function onYouTubeIframeAPIReady() {
	$(window).load(function () {
		$('.youtube-bg-iframe').each(function (index) {
			$(this).attr('id', 'yt-' + index);
			var player = new YT.Player($(this).attr('id'), {
				events: {
					'onReady': function () {
						player.mute();
						player.playVideo();
					},
					'onStateChange': function (newState) {
						player.playVideo();
					}
				}
			});
		});
	});

}