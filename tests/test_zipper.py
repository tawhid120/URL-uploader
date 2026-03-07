"""Tests for bot.helpers.zipper module."""

import os
import tempfile
import zipfile

from bot.helpers.zipper import create_zip


class TestCreateZip:
    def test_creates_zip_from_files(self):
        """ZIP file should contain all provided files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create sample files
            paths = []
            for i in range(3):
                fpath = os.path.join(tmpdir, f"file_{i}.txt")
                with open(fpath, "w") as f:
                    f.write(f"content {i}")
                paths.append(fpath)

            zip_path = os.path.join(tmpdir, "output.zip")
            result = create_zip(paths, zip_path)

            assert result == zip_path
            assert os.path.isfile(zip_path)

            with zipfile.ZipFile(zip_path, "r") as zf:
                names = zf.namelist()
                assert len(names) == 3
                assert "file_0.txt" in names
                assert "file_1.txt" in names
                assert "file_2.txt" in names

    def test_empty_list(self):
        """ZIP with no files should still be created (empty archive)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "empty.zip")
            result = create_zip([], zip_path)
            assert result == zip_path
            assert os.path.isfile(zip_path)

    def test_skips_missing_files(self):
        """Non-existent files in the list should be skipped gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real = os.path.join(tmpdir, "real.txt")
            with open(real, "w") as f:
                f.write("hello")
            fake = os.path.join(tmpdir, "fake.txt")

            zip_path = os.path.join(tmpdir, "mixed.zip")
            create_zip([real, fake], zip_path)

            with zipfile.ZipFile(zip_path, "r") as zf:
                assert len(zf.namelist()) == 1
