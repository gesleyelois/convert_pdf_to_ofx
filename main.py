"""
Aplicação principal para conversão de extratos PDF para OFX.
"""

from config import PDFS_DIR, OFXS_DIR
from services.logger import StructuredLogger
from services.file_validator import PDFFileValidator
from services.file_processor import PDFFileProcessor
from services.cleanup_service import CleanupService
from writers.ofx_writer import OFXWriterRefactored

class Extrato2OFXApp:
    def __init__(self):
        self.logger = StructuredLogger()
        self.ofx_writer = OFXWriterRefactored()
        self.file_processor = PDFFileProcessor(self.ofx_writer, self.logger)
        self.cleanup_service = CleanupService(self.logger)
        self.file_validator = PDFFileValidator()
    
    def run(self) -> None:
        try:
            self._setup_directories()
            self._process_pdf_files()
            self._cleanup_temp_files()
            self._log_summary()
        except Exception as e:
            self.logger.error(f"Erro crítico na aplicação: {e}")
            raise
    
    def _setup_directories(self) -> None:
        OFXS_DIR.mkdir(exist_ok=True)
        self.cleanup_service.ensure_temp_directory_exists()
        self.logger.info("Diretórios configurados com sucesso")
    
    def _process_pdf_files(self) -> None:
        self.logger.info("Iniciando conversão de PDFs em OFX...")
        pdf_files = self._get_valid_pdf_files()
        if not pdf_files:
            self.logger.warning("Nenhum arquivo PDF válido encontrado")
            return
        self.logger.info(f"Encontrados {len(pdf_files)} arquivos PDF para processar")
        successful_conversions = 0
        failed_conversions = 0
        for pdf_file in pdf_files:
            result = self.file_processor.process_file(str(pdf_file))
            if result.success:
                successful_conversions += 1
            else:
                failed_conversions += 1
        self.logger.info(
            f"Processamento concluído: {successful_conversions} sucessos, "
            f"{failed_conversions} falhas"
        )
    
    def _get_valid_pdf_files(self):
        if not PDFS_DIR.exists():
            self.logger.error(f"Diretório de PDFs não encontrado: {PDFS_DIR}")
            return []
        valid_files = []
        for file_path in PDFS_DIR.iterdir():
            if self.file_validator.is_valid_file(str(file_path)):
                valid_files.append(file_path)
        return valid_files
    
    def _cleanup_temp_files(self) -> None:
        self.cleanup_service.cleanup_temp_directory()
    
    def _log_summary(self) -> None:
        self.logger.info(f"Conversão concluída. Arquivos OFX gerados em: {OFXS_DIR}")

def main():
    app = Extrato2OFXApp()
    app.run()

if __name__ == '__main__':
    main() 