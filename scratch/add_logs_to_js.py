import os

root_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"

def update_dialog_js():
    path = os.path.join(root_dir, "js", "dialog.js")
    content = open(path, "r", encoding="utf-8", errors="ignore").read()
    
    old_show = "showDialog(){const{dialog}=this.refs;"
    new_show = 'showDialog(){console.log("[Dialog] showDialog called on:", this.id||this.tagName, "dialog open:", this.refs.dialog?.open);const{dialog}=this.refs;'
    
    old_close = "closeDialog=async()=>{const{dialog}=this.refs;"
    new_close = 'closeDialog=async()=>{console.log("[Dialog] closeDialog called on:", this.id||this.tagName);const{dialog}=this.refs;'
    
    modified = False
    if old_show in content:
        content = content.replace(old_show, new_show)
        modified = True
        print("Updated showDialog in dialog.js")
    else:
        # Check if space is different or minified differently
        print("Warning: showDialog signature not found exactly")
        
    if old_close in content:
        content = content.replace(old_close, new_close)
        modified = True
        print("Updated closeDialog in dialog.js")
    else:
        print("Warning: closeDialog signature not found exactly")
        
    if modified:
        open(path, "w", encoding="utf-8").write(content)

def update_section_renderer_js():
    path = os.path.join(root_dir, "js", "section-renderer.js")
    content = open(path, "r", encoding="utf-8", errors="ignore").read()
    
    old_morph = 'morph(existingElement,newElement)'
    new_morph = 'console.log("[SectionRenderer] morphSection dialog open states before morph:", Array.from(existingDialogs).map(d => d.open)); morph(existingElement,newElement)'
    
    if old_morph in content:
        content = content.replace(old_morph, new_morph)
        open(path, "w", encoding="utf-8").write(content)
        print("Updated morphSection in section-renderer.js")
    else:
        print("Warning: morphSection signature not found exactly")

if __name__ == "__main__":
    update_dialog_js()
    update_section_renderer_js()
