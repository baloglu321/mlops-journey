variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run deployment"
  type        = string
  default     = "europe-west3" #frankfurt
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "cyber-analyzer"
}

variable "openai_api_key" {
  description = "OpenAI API key for the application"
  type        = string
  sensitive   = true
  default     = ""
}

variable "semgrep_app_token" {
  description = "Semgrep app token for security scanning"
  type        = string
  sensitive   = true
  default     = ""
}

variable "docker_image_tag" {
  description = "Tag for the Docker image"
  type        = string
  default     = "latest"
}
variable "ollama_api_url" {
  description = "The Cloudflare Tunnel URL for the remote Ollama server (e.g., https://...trycloudflare.com)"
  type        = string
}

variable "openai_base_url" {
  description = "OpenAI Proxy or API Base URL address"
  type        = string
  default     = "http://127.0.0.1:4000"
  # Bu olmazsa Python kodu proxy yerine gerçek OpenAI'ye gitmeye çalışır ve 'Key Geçersiz' hatası alırsın.
}