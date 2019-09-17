from falcon import testing
from hcproxy.bootstrap import Bootstrap
from pytest_httpserver import HTTPServer
import pytest

good_report = "Duplicati%20Backup%20report%20for%20DevTest%0A%0ADeletedFiles%3A%200%0ADeletedFolders%3A%200%0AModifiedFiles%3A%200%0AExaminedFiles%3A%203%0AOpenedFiles%3A%203%0AAddedFiles%3A%203%0ASizeOfModifiedFiles%3A%200%0ASizeOfAddedFiles%3A%20324925%0ASizeOfExaminedFiles%3A%20324925%0ASizeOfOpenedFiles%3A%20324925%0ANotProcessedFiles%3A%200%0AAddedFolders%3A%201%0ATooLargeFiles%3A%200%0AFilesWithError%3A%200%0AModifiedFolders%3A%200%0AModifiedSymlinks%3A%200%0AAddedSymlinks%3A%200%0ADeletedSymlinks%3A%200%0APartialBackup%3A%20False%0ADryrun%3A%20False%0AMainOperation%3A%20Backup%0AParsedResult%3A%20Success%0AVersion%3A%202.0.4.5%20%282.0.4.5_beta_2018-11-28%29%0AEndTime%3A%202019-09-13%2012%3A48%3A55%20PM%20%281568393335%29%0ABeginTime%3A%202019-09-13%2012%3A48%3A54%20PM%20%281568393334%29%0ADuration%3A%2000%3A00%3A01.0164740"
failure_report = "Duplicati%20Backup%20report%20for%20DevTest%0A%0AFailed%3A%20Found%203%20files%20that%20are%20missing%20from%20the%20remote%20storage%2C%20please%20run%20repair%0ADetails%3A%20Duplicati.Library.Interface.UserInformationException%3A%20Found%203%20files%20that%20are%20missing%20from%20the%20remote%20storage%2C%20please%20run%20repair%0A%20%20at%20Duplicati.Library.Main.Operation.FilelistProcessor.VerifyRemoteList%20%28Duplicati.Library.Main.BackendManager%20backend%2C%20Duplicati.Library.Main.Options%20options%2C%20Duplicati.Library.Main.Database.LocalDatabase%20database%2C%20Duplicati.Library.Main.IBackendWriter%20log%2C%20System.String%20protectedfile%29%20%5B0x00203%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Operation.BackupHandler.PreBackupVerify%20%28Duplicati.Library.Main.BackendManager%20backend%2C%20System.String%20protectedfile%29%20%5B0x0010d%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Operation.BackupHandler.RunAsync%20%28System.String%5B%5D%20sources%2C%20Duplicati.Library.Utility.IFilter%20filter%29%20%5B0x01031%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20CoCoL.ChannelExtensions.WaitForTaskOrThrow%20%28System.Threading.Tasks.Task%20task%29%20%5B0x00050%5D%20in%20%3C6973ce2780de4b28aaa2c5ffc59993b1%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Operation.BackupHandler.Run%20%28System.String%5B%5D%20sources%2C%20Duplicati.Library.Utility.IFilter%20filter%29%20%5B0x00008%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Controller%2B%3C%3Ec__DisplayClass13_0.%3CBackup%3Eb__0%20%28Duplicati.Library.Main.BackupResults%20result%29%20%5B0x00035%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Controller.RunAction%5BT%5D%20%28T%20result%2C%20System.String%5B%5D%26%20paths%2C%20Duplicati.Library.Utility.IFilter%26%20filter%2C%20System.Action%601%5BT%5D%20method%29%20%5B0x0011d%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%0ALog%20data%3A%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BWarning-Duplicati.Library.Main.Controller-UnsupportedOption%5D%3A%20The%20supplied%20option%20--%2FUsers%2Fadenau%2Fgit%2FDevTest%2F%20is%20not%20supported%20and%20will%20be%20ignored%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BWarning-Duplicati.Library.Main.Operation.FilelistProcessor-MissingFile%5D%3A%20Missing%20file%3A%20duplicati-20190913T164855Z.dlist.zip%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BWarning-Duplicati.Library.Main.Operation.FilelistProcessor-MissingFile%5D%3A%20Missing%20file%3A%20duplicati-bc6b477861591419ab392cc3f45a73956.dblock.zip%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BWarning-Duplicati.Library.Main.Operation.FilelistProcessor-MissingFile%5D%3A%20Missing%20file%3A%20duplicati-ic344948b2cbc407aaff63711877af376.dindex.zip%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BError-Duplicati.Library.Main.Operation.FilelistProcessor-MissingRemoteFiles%5D%3A%20Found%203%20files%20that%20are%20missing%20from%20the%20remote%20storage%2C%20please%20run%20repair%0A2019-09-13%2012%3A50%3A36%20-04%20-%20%5BError-Duplicati.Library.Main.Operation.BackupHandler-FatalError%5D%3A%20Fatal%20error%0ADuplicati.Library.Interface.UserInformationException%3A%20Found%203%20files%20that%20are%20missing%20from%20the%20remote%20storage%2C%20please%20run%20repair%0A%20%20at%20Duplicati.Library.Main.Operation.FilelistProcessor.VerifyRemoteList%20%28Duplicati.Library.Main.BackendManager%20backend%2C%20Duplicati.Library.Main.Options%20options%2C%20Duplicati.Library.Main.Database.LocalDatabase%20database%2C%20Duplicati.Library.Main.IBackendWriter%20log%2C%20System.String%20protectedfile%29%20%5B0x00203%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Operation.BackupHandler.PreBackupVerify%20%28Duplicati.Library.Main.BackendManager%20backend%2C%20System.String%20protectedfile%29%20%5B0x0010d%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A%20%20at%20Duplicati.Library.Main.Operation.BackupHandler.RunAsync%20%28System.String%5B%5D%20sources%2C%20Duplicati.Library.Utility.IFilter%20filter%29%20%5B0x004fa%5D%20in%20%3Cc6c6871f516b48f59d88f9d731c3ea4d%3E%3A0%20%0A"

@pytest.fixture()
def client():
    
    bootstrap = Bootstrap()

    with HTTPServer() as httpserver:
    
        httpserver.expect_request("/f8edfeb0-4025-4996-add7-57364accabe3").respond_with_data("OK")
        httpserver.expect_request("/f8edfeb0-4025-4996-add7-57364accabe3/fail").respond_with_data("Fail")

        #url_for_success = httpserver.url_for("/f8edfeb0-4025-4996-add7-57364accabe3")
        #url_for_failure = httpserver.url_for("/f8edfeb0-4025-4996-add7-57364accabe3/fail")

    return testing.TestClient(bootstrap.create())

def test_success(client):
    
    result = client.simulate_post('/duplicati/f8edfeb0-4025-4996-add7-57364accabe3', body=good_report)

    assert result.text == "OK"

def test_failure(client):

    result = client.simulate_post('/duplicati/f8edfeb0-4025-4996-add7-57364accabe3/fail', body=failure_report)

    assert result.text == "Fail"
