use std::fs::File;
use std::path::Path;
use zip::ZipArchive;

pub fn inspect_apk(path: &Path) -> Result<(), Box<dyn std::error::Error>> {
    println!("Inspecting APK: {}", path.display());
    let file = File::open(path)?;
    let mut archive = ZipArchive::new(file)?;

    let mut has_manifest = false;
    let mut dex_count = 0;
    let mut architectures = Vec::new();

    for i in 0..archive.len() {
        let entry = archive.by_index(i)?;
        let name = entry.name().to_string();

        if name == "AndroidManifest.xml" {
            has_manifest = true;
        } else if name.ends_with(".dex") {
            dex_count += 1;
        } else if name.starts_with("lib/") {
            let parts: Vec<&str> = name.split('/').collect();
            if parts.len() > 1 && !architectures.contains(&parts[1].to_string()) {
                architectures.push(parts[1].to_string());
            }
        }
    }

    println!("Package valid: {}", has_manifest);
    println!("DEX bytecode files: {}", dex_count);
    if architectures.is_empty() {
        println!("Native libraries: None (Pure Java/Kotlin bytecode)");
    } else {
        println!("Native target architectures: {}", architectures.join(", "));
    }

    Ok(())
}
