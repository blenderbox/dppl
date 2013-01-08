name             "pxlpng"
maintainer       "Blenderbox"
maintainer_email "djablons@blenderbox.com"
license          "Apache 2.0"
description      "An opinionated deployment for Django applications"
long_description  IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.1.0"

%w{ database mysql }.each do |dep|
  depends dep
end

supports "ubuntu"
