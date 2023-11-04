
conditionally load the assets from Vite's server in development:

{% if debug %}
    <script type="module" src="http://localhost:3000/@vite/client"></script>
    <script type="module" src="http://localhost:3000/src/main.js"></script>
{% else %}
    <script type="module" src="{% static 'frontend/main.js' %}"></script>
{% endif %}