---
layout: single
permalink: /booking/
title: Booking Test Page
tagline: Booking a vist.
author_profile: true
classes: wide
header:
  image: /assets/images/splash/splash_history.jpg

---

## Workshops

{% capture workshop-oi-content %}
**Saving the ‘Oi** – An Amazing Seabird Workshop

<!-- Calendly link widget begin -->
<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
<script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
<a href="" class="btn btn--primary" onclick="Calendly.initPopupWidget({url: 'https://calendly.com/wildlabtiakitaiao/saving-the-oi-workshop?primary_color=ff0303&hide_gdpr_banner=1'});return false;">Book Now</a>
<!-- Calendly link widget end -->

{% endcapture %}

<div class="notice">
  {{ workshop-oi-content | markdownify }}
</div>


## Inline Booking

<!-- Calendly inline widget begin -->
<div class="calendly-inline-widget" data-url="https://calendly.com/wildlabtiakitaiao?hide_landing_page_details=1&hide_gdpr_banner=1&primary_color=fb0303" style="min-width:320px;height:2000px;"></div>
<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
<!-- Calendly inline widget end -->


<!-- Calendly badge widget begin -->
<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
<script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
<script type="text/javascript">window.onload = function() { Calendly.initBadgeWidget({ url: 'https://calendly.com/wildlabtiakitaiao?hide_landing_page_details=1&hide_gdpr_banner=1&primary_color=ff0303', text: 'Make a Booking', color: '#ff0303', textColor: '#ffffff', branding: false }); }</script>
<!-- Calendly badge widget end -->