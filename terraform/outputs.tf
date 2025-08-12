output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.website.bucket
}

output "s3_bucket_website_endpoint" {
  description = "Website endpoint for the S3 bucket"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.website.id
}

output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.website.domain_name
}

output "website_url" {
  description = "URL of the website"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "https://${aws_cloudfront_distribution.website.domain_name}"
}

output "route53_zone_id" {
  description = "Route53 hosted zone ID (if domain is configured)"
  value       = var.domain_name != "" ? aws_route53_zone.website[0].zone_id : null
}

output "route53_name_servers" {
  description = "Route53 name servers (if domain is configured)"
  value       = var.domain_name != "" ? aws_route53_zone.website[0].name_servers : null
}
