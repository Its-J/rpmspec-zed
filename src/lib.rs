// Language server support, based on https://github.com/mtorromeo/zed-rpmspec-language/blob/main/src/lib.rs

use zed_extension_api::{self as zed, settings::LspSettings, LanguageServerId, Result, Worktree};

const SERVER_BINARY: &str = "rpm_lsp_server";

struct RpmSpecExtension;

impl zed::Extension for RpmSpecExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        language_server_id: &LanguageServerId,
        worktree: &Worktree,
    ) -> Result<zed::Command> {
        let binary = LspSettings::for_worktree(language_server_id.as_ref(), worktree)
            .ok()
            .and_then(|settings| settings.binary);

        let command = binary
            .as_ref()
            .and_then(|binary| binary.path.clone())
            .or_else(|| worktree.which(SERVER_BINARY))
            .ok_or_else(|| {
                format!(
                    "{SERVER_BINARY} must be installed manually. See https://github.com/dcermak/rpm-spec-language-server."
                )
            })?;

        let mut args = vec!["--stdio".to_string()];
        if let Some(arguments) = binary.as_ref().and_then(|binary| binary.arguments.clone()) {
            args.extend(arguments.into_iter().filter(|arg| arg != "--stdio"));
        }

        let mut env = worktree.shell_env();
        if let Some(extra) = binary.and_then(|binary| binary.env) {
            env.extend(extra);
        }

        Ok(zed::Command { command, args, env })
    }
}

zed::register_extension!(RpmSpecExtension);
