package org.apache.slider.providers.tajo.funtests

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.FileSystem
import org.apache.hadoop.fs.Path
import org.apache.slider.funtest.framework.CommandTestBase
import org.apache.slider.funtest.framework.FuntestProperties
import org.junit.Before
import org.junit.Test

class ImagesIT extends CommandTestBase implements FuntestProperties {


    @Before
    public void verifyPreconditions() {
        assumeBoolOption(SLIDER_CONFIG, KEY_TEST_TAJO_ENABLED, true)
    }

    @Test
    public void testImageExists() throws Throwable {

        Configuration conf = loadSliderConf()
        String testImage = conf.get(KEY_TEST_TAJO_TAR)
        assert testImage
        Path path = new Path(testImage)
        FileSystem fs = FileSystem.get(
                path.toUri(),
                conf)
        assert fs.exists(path)
    }

    @Test
    public void testAppConfExists() throws Throwable {
        Configuration conf = loadSliderConf()
        String dir = conf.get(KEY_TEST_TAJO_APPCONF)

        assert conf.get(KEY_TEST_TAJO_APPCONF)
        Path path = new Path(dir)
        FileSystem fs = FileSystem.get(
                path.toUri(),
                conf)
        assert fs.exists(path)
    }
}
