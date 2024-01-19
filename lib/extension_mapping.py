word_extensions = [
    "doc",  # Legacy Word format
    "docx",  # Modern Word format
    "dot",  # Legacy Word template
    "dotx",  # Modern Word template
    "docm",  # Macro-enabled Word document
    "dotm",  # Macro-enabled Word template
    "rtf",  # Rich Text Format
    "odt",  # OpenDocument Text (supported in newer Word versions)
    "txt",  # Plain text (limited formatting)
    "htm", "html",  # Web pages (may open with formatting differences)
    "wps",  # WordPerfect document (supported in newer Word versions)
    "xml",  # Word XML format (for special cases)
]
app_word_mapping_dict= dict([(x[1:],"Word.Application") for x in word_extensions])

notepad_extensions = [
    "txt",  # Text files
    "log",  # Log files
    "bat",  # Batch files
    "cmd",  # Command files
    "ini",  # Configuration files
    "inf",  # Information files
    "reg",  # Registry files
    "csv",  # Comma-separated values files
    "html",  # HyperText Markup Language files
    "htm",  # HyperText Markup Language files (alternative extension)
    "js",  # JavaScript files
    "css",  # Cascading Style Sheets files
    "py",  # Python source code files
    "vbs",  # Visual Basic Script files
    "sql",  # Structured Query Language files
    "xml",  # Extensible Markup Language files
    "json",  # JavaScript Object Notation files
    "config",  # Configuration files (common extension)
    "props",  # Properties files
    "json"
]
powerpoint_extensions = [
    "ppt",  # PowerPoint 97-2003 Presentation
    "pptx",  # PowerPoint Presentation (Office Open XML)
    "pot",  # PowerPoint 97-2003 Template
    "potx",  # PowerPoint Template (Office Open XML)
    "pps",  # PowerPoint 97-2003 Slide Show
    "ppsx",  # PowerPoint Slide Show (Office Open XML)
    "ppa",  # PowerPoint Add-in
    "ppam",  # PowerPoint Add-in (Office Open XML)
    "sldm",  # PowerPoint Macro-Enabled Slide
    "sldx",  # PowerPoint Slide (Office Open XML)
    "odp",  # OpenDocument Presentation
    "thmx",  # PowerPoint Theme
    "pdf",  # Portable Document Format (view-only in most cases)
    "potm",  # PowerPoint Macro-Enabled Template
    "ppsm",  # PowerPoint Macro-Enabled Slide Show
    "pptm",  # PowerPoint Macro-Enabled Presentation
    "sldxm",  # PowerPoint Macro-Enabled Slide
]

excel_extensions = [
    "xls",  # Excel 97-2003 Workbook
    "xlsx",  # Excel Workbook (Office Open XML)
    "xltx",  # Excel Template (Office Open XML)
    "xltm",  # Excel Macro-Enabled Template
    "xlsm",  # Excel Macro-Enabled Workbook
    "xlsb",  # Excel Binary Workbook
    "xlam",  # Excel Add-in (Office Open XML)
    "ods",  # OpenDocument Spreadsheet
    "csv",  # Comma-Separated Values
    "tsv",  # Tab-Separated Values
    "txt",  # Text (often for delimited data)
    "prn",  # Printer output file
    "dif",  # Data Interchange Format
    "sylk",  # Symbolic Link
    "xml",  # XML Spreadsheet
    "htm",  # HTML (read-only)
    "html",  # HTML (read-only)
    "pdf",  # Portable Document Format (read-only in most cases)
    "xps",  # XML Paper Specification (read-only)
]

paint_extensions = [
    "bmp",  # Bitmap Image File
    "gif",  # Graphics Interchange Format
    "jpg",  "jpeg",  # Joint Photographic Experts Group
    "png",  # Portable Network Graphics
    "tif",  "tiff",  # Tagged Image File Format
    "ico",  # Icon File
    "jfif",  # JPEG File Interchange Format
    "dib",  # Device-Independent Bitmap
    "wdp",  # Windows Media Photo
    "hdp",  # High Dynamic Range Image
    "jxr",  # JPEG XR Image
    "wdp",  # Windows Media Photo
    "webp",  # Web Picture
]