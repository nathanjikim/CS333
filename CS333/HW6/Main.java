package hw6;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Main {

    public static class RC4 {
        private final byte[] S = new byte[256];
        private final byte[] T = new byte[256];
        private final int keylen;

        public RC4(final byte[] key) {
            keylen = key.length;
            for (int i = 0; i < 256; i++) {
                S[i] = (byte) i;
                T[i] = key[i % keylen];
            }
            int j = 0;
            byte tmp;
            for (int i = 0; i < 256; i++) {
                j = (j + S[i] + T[i]) & 0xFF;
                tmp = S[j];
                S[j] = S[i];
                S[i] = tmp;
            }
        }

        public byte[] decrypt(final byte[] ciphertext) {
            final byte[] result = new byte[ciphertext.length];
            int i = 0, j = 0, k, t;
            byte tmp;
            for (int counter = 0; counter < ciphertext.length; counter++) {
                i = (i + 1) & 0xFF;
                j = (j + S[i]) & 0xFF;
                tmp = S[j];
                S[j] = S[i];
                S[i] = tmp;
                t = (S[i] + S[j]) & 0xFF;
                k = S[t];
                result[counter] = (byte) (ciphertext[counter] ^ k);
            }
            return result;
        }
    }

    public static byte[] readFile(String filename)
    {
        byte[] result = new byte[100];
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            int counter = 0;
            while ((line = br.readLine()) != null) {
                String[] split = line.split(",");
                for(String s: split)
                {
                    if(counter == 100)
                    {
                        return result;
                    }
                    int i = Integer.parseInt(s);
                    byte b = (byte) i;
                    result[counter++] = b;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static BigInteger modularExponentiation(BigInteger a, BigInteger b, BigInteger m)
    {
        BigInteger x = BigInteger.valueOf(1);
        a = a.mod(m);
        while(b.compareTo(BigInteger.ZERO) > 0)
        {
            if(b.mod(BigInteger.TWO).equals(BigInteger.ONE))
            {
                x = (x.multiply(a)).mod(m);
            }
            a = (a.multiply(a)).mod(m);
            b = b.divide(BigInteger.TWO);
        }
        return x;
//        return a.modPow(b, m);
    }

    public static byte[] getKey(BigInteger ciphertext, BigInteger privateKey, BigInteger N)
    {
        BigInteger x = modularExponentiation(ciphertext, privateKey, N);
        byte[] key = x.toByteArray();
        return reverse(key);
    }


    public static byte[] reverse(byte[] arr)
    {
        byte[] result = new byte[arr.length];
        int j = arr.length;
        for(int i = 0; i < arr.length; i++)
        {
            result[j - 1] = arr[i];
            j--;
        }
        return result;
    }


    public static String decipher(BigInteger ciphertext, BigInteger privateKey, BigInteger N) throws UnsupportedEncodingException {
        BigInteger x = modularExponentiation(ciphertext, privateKey, N);
        byte[] b = reverse(x.toByteArray());
        String result = new String(b, "UTF8");
        return result;
    }

    public static boolean verify(BigInteger signature, BigInteger e, BigInteger N, String M) throws NoSuchAlgorithmException {
        BigInteger x = modularExponentiation(signature, e, N);
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = reverse(digest.digest(M.getBytes(StandardCharsets.UTF_8)));
        BigInteger y = new BigInteger(hash);
        return x.equals(y);
    }

    public static void main(String[] args) throws UnsupportedEncodingException, NoSuchAlgorithmException{
        BigInteger senderPublicN = new BigInteger("14767789088582292244976747471834622809030523389252301416499843578543747157288054303583250729820529188683838583836411200154694987101826052078028806429119601176181200668505289449621631137525108684399218471935323681677255077737021708528244344205767842493738283959811875248198673494621783005916640299371062353730727145692335246112465972798342793435955557505429543539832206467677204122477631578925311247739654924063858944809344461269057796112550255176042456414649900612467836821249929802868020381200595634502402342770214098221950244679695607363642167588212946638735024669548859833731040268128468907513672753");
        BigInteger senderPublicE = new BigInteger("23");

        BigInteger receiverPublicN = new BigInteger("14652249382231888581431334873087665335445949785812005119004278241374772864289460776540728431780047732549889984854429587370284165099891254675075438427840699599993460108718433235535197979843830130345930981094776292203593080766026756180504480959071004047720746406234564547195243298229881871012109102878887054188246027001044721685014474701052585708308821750817768356871032054682230424961248984365357905977075727034418656735843841124832448173031719870999596376671643379292875009532190125106772339865224792634326043231921436125360361361828145064805681985287560102988846483030416804351139009691625344427396289");
        BigInteger receiverPublicE = new BigInteger("3");

        BigInteger receiverPrivateD = new BigInteger("9768166254821259054287556582058443556963966523874670079336185494249848576192973851027152287853365155033259989902953058246856110066594169783383625618560466399995640072478955490356798653229220086897287320729850861469062053844017837453669653972714002698480497604156376364796828865486587914008072735252585627124142852315828861471516342247676689434041485207455088144363265259906449458938540907001405367845360730805078130453243161777057717863712208349209870623470284592818323753371370773677425185171570700929514006692491711433853230497905858135242630874435937587611042573566776670799108751826061345088493827");

        BigInteger message1cipher = new BigInteger("17744666925916274621612910542654898807142941672528240327155702703024634550702997421237721270966529482028915994314773271545948740337732134642404138895881506799292838543181769803146449278896630272");
        BigInteger message1sig = new BigInteger("10807022412217594710114173202348067802389675636129087117571281315421574190197544578198319276399268378293628887674900247319717110989786504024348635092077726408464799755250969730209046043072467848799926127759614410937938095692088610904896174892737712395488733805805539801592903322925826233329214764495351999922592766362346412255050951697421804384487443273905695447066146652296858919070087159329546567516546294366115606594821191981861391199907333355558309800103861072824953600778494502072149070282654785915274682323075094266823774280458225839103821531730848305705634428291957983874853580395177633880979708");
        BigInteger message2cipher = new BigInteger("147564469888816812893586145835528899371307534912727235629274933089931434460499694024046870161935102749596945002877773213260723067342999888772449746026935860857887969410808928445918123524708538693027833229363308142005615390849488248076668602896440098923791192933008947918685795298045213354931486740188810081101778484247214844384669200141108892431471073908130125");
        BigInteger message2sig = new BigInteger("6608129893226312105340503657675010536973727447074532528345513125843360220715783393496667937123421465421836710614878616667699535400320495760962627076671257544274114429378783491918377907320742092804037257486687495942889836471225184512481775841000172503196009715767795535665835474313754321650971330447104974969627014108406462401538540501736292948321413724419760843812324970048895418084476763879904280969500182745896194140985127608088215506119431133901054333237493083016185915494816357253388608532987509608451070611989493212343809839843463459540634188737565147795264901668723708384935507608477095675040027");
        BigInteger message3cipher = new BigInteger("87751730142181862128758991007172007221296098736629573195220976506690318684001658707362187542114347248798512704000");
        BigInteger message3sig = new BigInteger("9343363784893130707911074207672793724517838962871720890406052216440677579664937040904848488185154173786373358227110196397777504423996544848441646914089878181337115113622141634320520840335376427261151337877448437967880345495723245803995214398006751533760011631517446484262752629798807650578920134298210363819124808893430665507063321591197715001107817918515940171267594498816089280525688182761225013741000371199968816311046780372096663155483479196942529535647275080962692803803306544526850357444267858810917709557944860824093939526833946713502519368943616802188210793521655082008934979682503629747632822");

        String message1 = decipher(message1cipher, receiverPrivateD, receiverPublicN);
        System.out.println(message1);
        System.out.println(verify(message1sig, senderPublicE, senderPublicN, message1));

        String message2 = decipher(message2cipher, receiverPrivateD, receiverPublicN);
        byte[] key = getKey(message2cipher, receiverPrivateD, receiverPublicN);
        System.out.println(message2);
        System.out.println(verify(message2sig, senderPublicE, senderPublicN, message2));

        String message3 = decipher(message3cipher, receiverPrivateD, receiverPublicN);
        System.out.println(message3);
        System.out.println(verify(message3sig, senderPublicE, senderPublicN, message3));

        RC4 cipher = new RC4(key);

        byte[] ciphertext = readFile("messageBig.txt");
        System.out.println(ciphertext);

        String s = new String(cipher.decrypt(ciphertext), "UTF8");

        System.out.println(s);
    }
}
