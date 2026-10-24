use clap::{Parser, Subcommand};
use std::path::PathBuf;

mod apk;
mod runtime;
mod repository;

#[derive(Parser)]
#[command(name = "fdroid-linux")]
#[command(about = "Ultra-lightweight Android / F-Droid compatibility layer for Linux", long_about = None)]
#[command(version = "0.1.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Inspect or extract an Android APK file
    Inspect {
        /// Path to the APK file
        apk_path: PathBuf,
    },
    /// Run an Android APK using the optimized native runtime layer
    Run {
        /// Path to the APK file
        apk_path: PathBuf,
        /// Optional extra arguments to pass to the runtime
        #[arg(trailing_var_arg = true)]
        args: Vec<String>,
    },
    /// Search and install applications directly from the official F-Droid repository
    Install {
        /// Package identifier or search term (e.g. org.fdroid.fdroid)
        package_id: String,
    },
    /// Check system dependencies and kernel environment (ashmem, binder, wayland)
    Doctor,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init();
    let cli = Cli::parse();

    match cli.command {
        Commands::Inspect { apk_path } => {
            apk::inspect_apk(&apk_path)?;
        }
        Commands::Run { apk_path, args } => {
            runtime::run_apk(&apk_path, &args)?;
        }
        Commands::Install { package_id } => {
            repository::install_from_fdroid(&package_id)?;
        }
        Commands::Doctor => {
            runtime::check_system_health();
        }
    }

    Ok(())
}
