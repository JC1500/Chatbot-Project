

echo "Creating .streamlit directory..."
mkdir -p /app/.streamlit

echo "Writing secrets.toml..."
cat <<EOF > /app/.streamlit/secrets.toml
[auth]
redirect_uri = "$OIDC_REDIRECT_URI"
cookie_secret = "$OIDC_COOKIE_SECRET"
client_id = "$OIDC_CLIENT_ID"
client_secret = "$OIDC_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
EOF

echo "Secrets file generated successfully."
cat /app/.streamlit/secrets.toml


exec streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0