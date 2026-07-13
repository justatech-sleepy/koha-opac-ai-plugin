# Koha OPAC Integration

To load the plugin inside Koha OPAC, edit:

```text
/usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/en/includes/opac-bottom.inc
```

Add the following before the closing `</body>` tag:

```html
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/variables.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/theme.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/chatbot.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/components.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/animations.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/responsive.css">

<script src="/opac-tmpl/bootstrap/js/config.js"></script>
<script src="/opac-tmpl/bootstrap/js/knowledgeBase.js"></script>
<script src="/opac-tmpl/bootstrap/js/faq.js"></script>
<script src="/opac-tmpl/bootstrap/js/intentEngine.js"></script>
<script src="/opac-tmpl/bootstrap/js/utils.js"></script>
<script src="/opac-tmpl/bootstrap/js/api.js"></script>
<script src="/opac-tmpl/bootstrap/js/chatController.js"></script>
<script src="/opac-tmpl/bootstrap/js/ui.js"></script>
<script src="/opac-tmpl/bootstrap/js/app.js"></script>
```
