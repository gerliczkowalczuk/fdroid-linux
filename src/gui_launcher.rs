use std::process::Command;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("==> Launching F-Droid Desktop GUI Client...");

    // Try standard system installed location first, then local source path
    let script_locations = [
        "/usr/share/fdroid/ui/app.py",
        "/home/oskargerliczkowalczuk/Projekty/germaz/fdroid-linux/ui/app.py",
    ];

    let mut launched = false;
    for script in &script_locations {
        if std::path::Path::new(script).exists() {
            let status = Command::new("python3")
                .arg(script)
                .args(std::env::args().skip(1))
                .status();
            if let Ok(st) = status {
                if st.success() {
                    launched = true;
                    break;
                }
            }
        }
    }

    if !launched {
        eprintln!("Error: Could not locate F-Droid GUI frontend script.");
    }

    Ok(())
}
